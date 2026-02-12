"""Cook session API endpoints."""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException

from ..models.schemas import (
    CookSetupRequest,
    CookSetupResponse,
    BackwardPlanResponse,
    FinishCookRequest,
    LidOpenRequest,
    PredictionResponse,
    ProbeReadingRequest,
    ReadingResponse,
    ReportResponse,
    StateResponse,
    WrapRequest,
    WrapResponse,
)
from ..services import cook_session_service as svc

router = APIRouter(prefix="/api/v1/cook", tags=["cook"])


def _prediction_to_response(pred, session_created_at=None) -> PredictionResponse:
    """Convert PredictionResult to PredictionResponse with absolute times."""
    base_time = session_created_at or datetime.utcnow()
    return PredictionResponse(
        p10_minutes=pred.p10_minutes,
        p50_minutes=pred.p50_minutes,
        p90_minutes=pred.p90_minutes,
        p10_time=base_time + timedelta(minutes=pred.p10_minutes),
        p50_time=base_time + timedelta(minutes=pred.p50_minutes),
        p90_time=base_time + timedelta(minutes=pred.p90_minutes),
        confidence=pred.confidence,
        current_state=pred.current_state,
        stall_probability=pred.stall_probability,
        readings_count=pred.readings_count,
    )


@router.post("/setup", response_model=CookSetupResponse)
async def setup_cook(request: CookSetupRequest):
    """Create a new cook session, fetch weather, run initial MC."""
    session, prediction, backward_plan = await svc.create_session(request)

    bp_response = None
    if backward_plan:
        bp_response = BackwardPlanResponse(
            dinner_time=backward_plan.dinner_time,
            fire_start_time=backward_plan.fire_start_time,
            meat_on_time=backward_plan.meat_on_time,
            estimated_cook_minutes_p90=backward_plan.estimated_cook_minutes_p90,
            rest_minutes=backward_plan.rest_minutes,
            preheat_minutes=backward_plan.preheat_minutes,
        )

    return CookSetupResponse(
        session_id=session.id,
        prediction=_prediction_to_response(prediction, session.created_at),
        backward_plan=bp_response,
    )


@router.post("/{session_id}/reading", response_model=ReadingResponse)
async def add_reading(session_id: str, request: ProbeReadingRequest):
    """Log a probe temperature reading."""
    try:
        session, prediction = await svc.add_reading(session_id, request)
    except ValueError:
        raise HTTPException(status_code=404, detail="Session not found")

    elapsed = session.readings[-1].elapsed_minutes if session.readings else 0.0

    return ReadingResponse(
        elapsed_minutes=elapsed,
        prediction=_prediction_to_response(prediction, session.created_at),
        state=StateResponse(
            current_state=session.current_state,
            confidence=session.confidence,
            stall_active=session.stall.in_stall,
            stall_duration_minutes=session.stall.stall_duration_minutes,
            wrap_type=session.wrap_type,
            readings_count=len(session.readings),
            elapsed_minutes=elapsed,
        ),
    )


@router.post("/{session_id}/lid-open")
async def lid_open(session_id: str, request: LidOpenRequest = LidOpenRequest()):
    """Log a lid-open event."""
    await svc.log_lid_open(session_id, request.duration_seconds)
    return {"status": "ok"}


@router.post("/{session_id}/wrap", response_model=WrapResponse)
async def apply_wrap(session_id: str, request: WrapRequest):
    """Log wrap decision, adjust model, re-run MC."""
    try:
        session, prediction, message = await svc.apply_wrap(session_id, request)
    except ValueError:
        raise HTTPException(status_code=404, detail="Session not found")

    return WrapResponse(
        wrap_type=request.wrap_type,
        prediction=_prediction_to_response(prediction, session.created_at),
        message=message,
    )


@router.get("/{session_id}/prediction", response_model=PredictionResponse)
async def get_prediction(session_id: str):
    """Get the latest cached prediction."""
    pred = await svc.get_prediction(session_id)
    if pred is None:
        raise HTTPException(status_code=404, detail="No prediction found")

    session = await svc.get_session(session_id)
    base_time = session.created_at if session else datetime.utcnow()
    return _prediction_to_response(pred, base_time)


@router.get("/{session_id}/state", response_model=StateResponse)
async def get_state(session_id: str):
    """Get current cook state and confidence."""
    session = await svc.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    elapsed = session.readings[-1].elapsed_minutes if session.readings else 0.0
    return StateResponse(
        current_state=session.current_state,
        confidence=session.confidence,
        stall_active=session.stall.in_stall,
        stall_duration_minutes=session.stall.stall_duration_minutes,
        wrap_type=session.wrap_type,
        readings_count=len(session.readings),
        elapsed_minutes=elapsed,
    )


@router.post("/{session_id}/finish", response_model=ReportResponse)
async def finish_cook(session_id: str, request: FinishCookRequest = FinishCookRequest()):
    """End cook and compute report."""
    try:
        report = await svc.finish_cook(session_id, request)
    except ValueError:
        raise HTTPException(status_code=404, detail="Session not found")

    return ReportResponse(
        session_id=report.session_id,
        total_cook_minutes=report.total_cook_minutes,
        final_temp_f=report.final_temp_f,
        stall_occurred=report.stall_occurred,
        stall_duration_minutes=report.stall_duration_minutes,
        was_wrapped=report.was_wrapped,
        wrap_type=report.wrap_type,
        prediction_accuracy_minutes=report.prediction_accuracy_minutes,
        readings_count=report.readings_count,
        lid_opens_count=report.lid_opens_count,
        quality_rating=report.quality_rating,
        quality_notes=report.quality_notes,
        predicted_temps=report.predicted_temps,
        actual_temps=report.actual_temps,
        residuals=report.residuals,
    )


@router.get("/{session_id}/report", response_model=ReportResponse)
async def get_report(session_id: str):
    """Get post-cook report for a finished session."""
    report = await svc.get_report(session_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    return ReportResponse(
        session_id=report.session_id,
        total_cook_minutes=report.total_cook_minutes,
        final_temp_f=report.final_temp_f,
        stall_occurred=report.stall_occurred,
        stall_duration_minutes=report.stall_duration_minutes,
        was_wrapped=report.was_wrapped,
        wrap_type=report.wrap_type,
        prediction_accuracy_minutes=report.prediction_accuracy_minutes,
        readings_count=report.readings_count,
        lid_opens_count=report.lid_opens_count,
        quality_rating=report.quality_rating,
        quality_notes=report.quality_notes,
        predicted_temps=report.predicted_temps,
        actual_temps=report.actual_temps,
        residuals=report.residuals,
    )
