"""Main orchestrator: ties together state machine, MC engine, trust, weather, DB.

This is the central service that coordinates all cook session operations.
"""

import uuid
from datetime import datetime
from typing import Optional

from ..models.enums import CookState, WrapType
from ..models.dataclasses import (
    BackwardPlan,
    CookSession,
    InterventionEvent,
    LidOpenEvent,
    PostCookReport,
    PredictionResult,
    ProbeReading,
    WeatherSnapshot,
)
from ..models.schemas import (
    CookSetupRequest,
    FinishCookRequest,
    ProbeReadingRequest,
    WrapRequest,
)
from ..simulation.monte_carlo import run_monte_carlo
from ..state_machine.cook_states import CookStateMachine
from ..state_machine.trust import TrustEvaluator
from ..planning.backward_planner import compute_backward_plan
from ..planning.wrap_intervention import get_wrap_tradeoff, should_suggest_wrap
from ..services.weather_service import fetch_weather
from ..database import repository as repo
from ..services.logging_service import log_event


# In-memory trust evaluators per session
_trust_evaluators: dict[str, TrustEvaluator] = {}


def _get_trust(session_id: str) -> TrustEvaluator:
    if session_id not in _trust_evaluators:
        _trust_evaluators[session_id] = TrustEvaluator()
    return _trust_evaluators[session_id]


async def create_session(
    request: CookSetupRequest,
) -> tuple[CookSession, PredictionResult, Optional[BackwardPlan]]:
    """Create a new cook session, fetch weather, run initial MC.

    Returns:
        (session, prediction, backward_plan or None)
    """
    session_id = str(uuid.uuid4())[:8]

    # Fetch weather if location provided
    weather: Optional[WeatherSnapshot] = None
    if request.latitude is not None and request.longitude is not None:
        weather = await fetch_weather(request.latitude, request.longitude)

    session = CookSession(
        id=session_id,
        created_at=datetime.utcnow(),
        meat_category=request.meat_category,
        cut_type=request.cut_type,
        weight_lbs=request.weight_lbs,
        thickness_inches=request.thickness_inches,
        equipment_type=request.equipment_type,
        smoker_temp_f=request.smoker_temp_f,
        target_temp_f=request.target_temp_f,
        dinner_time=request.dinner_time,
        altitude_ft=request.altitude_ft,
        weather=weather,
        current_state=CookState.PREHEAT,
    )

    # Run initial MC prediction
    prediction = run_monte_carlo(session, n_iterations=1000)  # fewer for initial
    prediction.session_id = session_id
    session.predictions.append(prediction)

    # Backward plan if dinner time specified
    backward_plan = None
    if request.dinner_time:
        backward_plan = compute_backward_plan(request.dinner_time, prediction)

    # Save to DB
    await repo.save_session(session)
    await repo.save_prediction(prediction)

    log_event("session_created", session_id=session_id,
              cut=request.cut_type.value, weight=request.weight_lbs)

    return session, prediction, backward_plan


async def add_reading(
    session_id: str, request: ProbeReadingRequest
) -> tuple[CookSession, PredictionResult]:
    """Log a probe temperature reading, advance state, re-run MC.

    Returns:
        (updated session, new prediction)
    """
    session = await repo.load_session(session_id)
    if session is None:
        raise ValueError(f"Session {session_id} not found")

    # Compute elapsed time
    elapsed = 0.0
    if session.readings:
        # Assume readings come ~every minute, or compute from timestamps
        elapsed = session.readings[-1].elapsed_minutes + 1.0

    reading = ProbeReading(
        session_id=session_id,
        timestamp=datetime.utcnow(),
        temp_f=request.temp_f,
        smoker_temp_f=request.smoker_temp_f,
        elapsed_minutes=elapsed,
    )

    await repo.save_reading(reading)
    session.readings.append(reading)

    # Advance state machine
    sm = CookStateMachine(session)
    sm.advance(reading)

    # Run MC with updated data
    prediction = run_monte_carlo(session, n_iterations=1000)
    prediction.session_id = session_id

    # Evaluate trust
    trust = _get_trust(session_id)
    prediction.confidence = trust.evaluate(session, prediction)
    session.confidence = prediction.confidence

    await repo.save_prediction(prediction)
    await repo.update_session_state(
        session_id, session.current_state.value, session.confidence.value
    )

    log_event("reading_added", session_id=session_id,
              temp=request.temp_f, state=session.current_state.value)

    return session, prediction


async def apply_wrap(
    session_id: str, request: WrapRequest
) -> tuple[CookSession, PredictionResult, str]:
    """Log wrap decision, adjust model, re-run MC.

    Returns:
        (updated session, new prediction, tradeoff message)
    """
    session = await repo.load_session(session_id)
    if session is None:
        raise ValueError(f"Session {session_id} not found")

    current_temp = session.readings[-1].temp_f if session.readings else 160.0
    elapsed = session.readings[-1].elapsed_minutes if session.readings else 0.0

    intervention = InterventionEvent(
        session_id=session_id,
        timestamp=datetime.utcnow(),
        wrap_type=request.wrap_type,
        temp_at_wrap_f=current_temp,
        elapsed_minutes=elapsed,
    )

    await repo.save_intervention(intervention)
    session.interventions.append(intervention)
    session.wrap_type = request.wrap_type

    # Re-run MC with wrap applied
    prediction = run_monte_carlo(session, n_iterations=1000)
    prediction.session_id = session_id

    trust = _get_trust(session_id)
    prediction.confidence = trust.evaluate(session, prediction)

    await repo.save_prediction(prediction)
    await repo.update_session_state(
        session_id, session.current_state.value,
        session.confidence.value, request.wrap_type.value
    )

    tradeoff = get_wrap_tradeoff(request.wrap_type)
    message = f"{tradeoff['title']}: {tradeoff['effect']}"

    log_event("wrap_applied", session_id=session_id,
              wrap_type=request.wrap_type.value)

    return session, prediction, message


async def log_lid_open(session_id: str, duration_seconds: float = 30.0) -> None:
    """Log a lid-open event."""
    event = LidOpenEvent(
        session_id=session_id,
        timestamp=datetime.utcnow(),
        duration_seconds=duration_seconds,
    )
    await repo.save_lid_event(event)
    log_event("lid_opened", session_id=session_id, duration=duration_seconds)


async def finish_cook(
    session_id: str, request: FinishCookRequest
) -> PostCookReport:
    """End cook, compute post-cook report."""
    session = await repo.load_session(session_id)
    if session is None:
        raise ValueError(f"Session {session_id} not found")

    await repo.finish_session(
        session_id,
        quality_rating=request.quality_rating.value if request.quality_rating else None,
        quality_notes=request.quality_notes,
    )

    # Build report
    actual_temps = [r.temp_f for r in session.readings]
    total_minutes = session.readings[-1].elapsed_minutes if session.readings else 0.0
    final_temp = actual_temps[-1] if actual_temps else 0.0

    # Get predicted temps from latest prediction for comparison
    predicted_temps: list[float] = []
    residuals: list[float] = []
    if session.predictions:
        # Simple linear interpolation from start to predicted finish
        pred = session.predictions[-1]
        n = len(actual_temps)
        if n > 0 and pred.p50_minutes > 0:
            for i in range(n):
                frac = (i / max(n - 1, 1))
                pred_temp = 40.0 + frac * (session.target_temp_f - 40.0)
                predicted_temps.append(round(pred_temp, 1))
                residuals.append(round(actual_temps[i] - pred_temp, 1))

    # Prediction accuracy: how far off was P50 from actual total time?
    accuracy = 0.0
    if session.predictions:
        accuracy = abs(session.predictions[-1].p50_minutes - total_minutes)

    report = PostCookReport(
        session_id=session_id,
        total_cook_minutes=total_minutes,
        final_temp_f=final_temp,
        stall_occurred=session.stall.in_stall or session.stall.stall_duration_minutes > 0,
        stall_duration_minutes=session.stall.stall_duration_minutes,
        was_wrapped=session.wrap_type != WrapType.NONE,
        wrap_type=session.wrap_type,
        prediction_accuracy_minutes=round(accuracy, 1),
        readings_count=len(session.readings),
        lid_opens_count=len(session.lid_events),
        quality_rating=request.quality_rating,
        quality_notes=request.quality_notes,
        predicted_temps=predicted_temps,
        actual_temps=actual_temps,
        residuals=residuals,
    )

    log_event("cook_finished", session_id=session_id,
              total_minutes=total_minutes, final_temp=final_temp)

    return report


async def get_prediction(session_id: str) -> Optional[PredictionResult]:
    """Get latest cached prediction for a session."""
    session = await repo.load_session(session_id)
    if session is None:
        return None
    return session.predictions[-1] if session.predictions else None


async def get_session(session_id: str) -> Optional[CookSession]:
    """Load a session from the database."""
    return await repo.load_session(session_id)


async def get_report(session_id: str) -> Optional[PostCookReport]:
    """Build a report for a finished session."""
    session = await repo.load_session(session_id)
    if session is None or not session.is_finished:
        return None

    actual_temps = [r.temp_f for r in session.readings]
    total_minutes = session.readings[-1].elapsed_minutes if session.readings else 0.0
    final_temp = actual_temps[-1] if actual_temps else 0.0

    predicted_temps: list[float] = []
    residuals: list[float] = []
    n = len(actual_temps)
    if n > 0:
        for i in range(n):
            frac = i / max(n - 1, 1)
            pred_temp = 40.0 + frac * (session.target_temp_f - 40.0)
            predicted_temps.append(round(pred_temp, 1))
            residuals.append(round(actual_temps[i] - pred_temp, 1))

    accuracy = 0.0
    if session.predictions:
        accuracy = abs(session.predictions[-1].p50_minutes - total_minutes)

    return PostCookReport(
        session_id=session_id,
        total_cook_minutes=total_minutes,
        final_temp_f=final_temp,
        stall_occurred=session.stall.stall_duration_minutes > 0,
        stall_duration_minutes=session.stall.stall_duration_minutes,
        was_wrapped=session.wrap_type != WrapType.NONE,
        wrap_type=session.wrap_type,
        prediction_accuracy_minutes=round(accuracy, 1),
        readings_count=len(session.readings),
        lid_opens_count=len(session.lid_events),
        predicted_temps=predicted_temps,
        actual_temps=actual_temps,
        residuals=residuals,
    )
