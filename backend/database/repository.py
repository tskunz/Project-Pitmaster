"""CRUD operations for cook session data."""

from datetime import datetime
from typing import Optional
import aiosqlite

from .db import get_db
from ..models.dataclasses import (
    CookSession,
    InterventionEvent,
    LidOpenEvent,
    PredictionResult,
    ProbeReading,
    WeatherSnapshot,
)
from ..models.enums import (
    ConfidenceTier,
    CookState,
    CutType,
    EquipmentType,
    MeatCategory,
    QualityRating,
    WrapType,
)


async def save_session(session: CookSession) -> None:
    """Insert or update a cook session."""
    db = await get_db()
    await db.execute(
        """
        INSERT INTO cook_sessions
            (id, created_at, meat_category, cut_type, weight_lbs,
             thickness_inches, equipment_type, smoker_temp_f, target_temp_f,
             dinner_time, altitude_ft, wrap_type, current_state, confidence,
             weather_ambient_temp, weather_wind_speed, weather_humidity,
             is_finished, quality_rating, quality_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            wrap_type=excluded.wrap_type,
            current_state=excluded.current_state,
            confidence=excluded.confidence,
            is_finished=excluded.is_finished,
            quality_rating=excluded.quality_rating,
            quality_notes=excluded.quality_notes
        """,
        (
            session.id,
            session.created_at.isoformat(),
            session.meat_category.value,
            session.cut_type.value,
            session.weight_lbs,
            session.thickness_inches,
            session.equipment_type.value,
            session.smoker_temp_f,
            session.target_temp_f,
            session.dinner_time.isoformat() if session.dinner_time else None,
            session.altitude_ft,
            session.wrap_type.value,
            session.current_state.value,
            session.confidence.value,
            session.weather.ambient_temp_f if session.weather else None,
            session.weather.wind_speed_mph if session.weather else None,
            session.weather.humidity_pct if session.weather else None,
            1 if session.is_finished else 0,
            None,
            "",
        ),
    )
    await db.commit()


async def load_session(session_id: str) -> Optional[CookSession]:
    """Load a cook session with all related data."""
    db = await get_db()
    cursor = await db.execute(
        "SELECT * FROM cook_sessions WHERE id = ?", (session_id,)
    )
    row = await cursor.fetchone()
    if row is None:
        return None

    session = CookSession(
        id=row["id"],
        created_at=datetime.fromisoformat(row["created_at"]),
        meat_category=MeatCategory(row["meat_category"]),
        cut_type=CutType(row["cut_type"]),
        weight_lbs=row["weight_lbs"],
        thickness_inches=row["thickness_inches"],
        equipment_type=EquipmentType(row["equipment_type"]),
        smoker_temp_f=row["smoker_temp_f"],
        target_temp_f=row["target_temp_f"],
        dinner_time=(
            datetime.fromisoformat(row["dinner_time"])
            if row["dinner_time"]
            else None
        ),
        altitude_ft=row["altitude_ft"],
        wrap_type=WrapType(row["wrap_type"]),
        current_state=CookState(row["current_state"]),
        confidence=ConfidenceTier(row["confidence"]),
        is_finished=bool(row["is_finished"]),
    )

    if row["weather_ambient_temp"] is not None:
        session.weather = WeatherSnapshot(
            ambient_temp_f=row["weather_ambient_temp"],
            wind_speed_mph=row["weather_wind_speed"] or 5.0,
            humidity_pct=row["weather_humidity"] or 50.0,
        )

    # Load readings
    cursor = await db.execute(
        "SELECT * FROM probe_readings WHERE session_id = ? ORDER BY elapsed_minutes",
        (session_id,),
    )
    rows = await cursor.fetchall()
    session.readings = [
        ProbeReading(
            id=r["id"],
            session_id=r["session_id"],
            timestamp=datetime.fromisoformat(r["timestamp"]),
            temp_f=r["temp_f"],
            smoker_temp_f=r["smoker_temp_f"],
            elapsed_minutes=r["elapsed_minutes"],
        )
        for r in rows
    ]

    # Load lid events
    cursor = await db.execute(
        "SELECT * FROM lid_open_events WHERE session_id = ? ORDER BY timestamp",
        (session_id,),
    )
    rows = await cursor.fetchall()
    session.lid_events = [
        LidOpenEvent(
            id=r["id"],
            session_id=r["session_id"],
            timestamp=datetime.fromisoformat(r["timestamp"]),
            duration_seconds=r["duration_seconds"],
        )
        for r in rows
    ]

    # Load interventions
    cursor = await db.execute(
        "SELECT * FROM intervention_events WHERE session_id = ? ORDER BY timestamp",
        (session_id,),
    )
    rows = await cursor.fetchall()
    session.interventions = [
        InterventionEvent(
            id=r["id"],
            session_id=r["session_id"],
            timestamp=datetime.fromisoformat(r["timestamp"]),
            wrap_type=WrapType(r["wrap_type"]),
            temp_at_wrap_f=r["temp_at_wrap_f"],
            elapsed_minutes=r["elapsed_minutes"],
        )
        for r in rows
    ]

    # Load latest prediction
    cursor = await db.execute(
        "SELECT * FROM predictions WHERE session_id = ? ORDER BY timestamp DESC LIMIT 1",
        (session_id,),
    )
    pred_row = await cursor.fetchone()
    if pred_row:
        session.predictions = [
            PredictionResult(
                id=pred_row["id"],
                session_id=pred_row["session_id"],
                timestamp=datetime.fromisoformat(pred_row["timestamp"]),
                p10_minutes=pred_row["p10_minutes"],
                p50_minutes=pred_row["p50_minutes"],
                p90_minutes=pred_row["p90_minutes"],
                confidence=ConfidenceTier(pred_row["confidence"]),
                current_state=CookState(pred_row["current_state"]),
                stall_probability=pred_row["stall_probability"],
                readings_count=pred_row["readings_count"],
            )
        ]

    return session


async def save_reading(reading: ProbeReading) -> int:
    """Save a probe reading. Returns the new row ID."""
    db = await get_db()
    cursor = await db.execute(
        """
        INSERT INTO probe_readings (session_id, timestamp, temp_f, smoker_temp_f, elapsed_minutes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            reading.session_id,
            reading.timestamp.isoformat(),
            reading.temp_f,
            reading.smoker_temp_f,
            reading.elapsed_minutes,
        ),
    )
    await db.commit()
    return cursor.lastrowid


async def save_lid_event(event: LidOpenEvent) -> int:
    """Save a lid-open event."""
    db = await get_db()
    cursor = await db.execute(
        """
        INSERT INTO lid_open_events (session_id, timestamp, duration_seconds)
        VALUES (?, ?, ?)
        """,
        (event.session_id, event.timestamp.isoformat(), event.duration_seconds),
    )
    await db.commit()
    return cursor.lastrowid


async def save_intervention(event: InterventionEvent) -> int:
    """Save an intervention event."""
    db = await get_db()
    cursor = await db.execute(
        """
        INSERT INTO intervention_events (session_id, timestamp, wrap_type, temp_at_wrap_f, elapsed_minutes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            event.session_id,
            event.timestamp.isoformat(),
            event.wrap_type.value,
            event.temp_at_wrap_f,
            event.elapsed_minutes,
        ),
    )
    await db.commit()
    return cursor.lastrowid


async def save_prediction(prediction: PredictionResult) -> int:
    """Save a prediction result."""
    db = await get_db()
    cursor = await db.execute(
        """
        INSERT INTO predictions
            (session_id, timestamp, p10_minutes, p50_minutes, p90_minutes,
             confidence, current_state, stall_probability, readings_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            prediction.session_id,
            prediction.timestamp.isoformat(),
            prediction.p10_minutes,
            prediction.p50_minutes,
            prediction.p90_minutes,
            prediction.confidence.value,
            prediction.current_state.value,
            prediction.stall_probability,
            prediction.readings_count,
        ),
    )
    await db.commit()
    return cursor.lastrowid


async def update_session_state(
    session_id: str, state: str, confidence: str, wrap_type: str | None = None
) -> None:
    """Update session state fields."""
    db = await get_db()
    if wrap_type:
        await db.execute(
            "UPDATE cook_sessions SET current_state=?, confidence=?, wrap_type=? WHERE id=?",
            (state, confidence, wrap_type, session_id),
        )
    else:
        await db.execute(
            "UPDATE cook_sessions SET current_state=?, confidence=? WHERE id=?",
            (state, confidence, session_id),
        )
    await db.commit()


async def finish_session(
    session_id: str,
    quality_rating: str | None = None,
    quality_notes: str = "",
) -> None:
    """Mark session as finished."""
    db = await get_db()
    await db.execute(
        "UPDATE cook_sessions SET is_finished=1, current_state='done', quality_rating=?, quality_notes=? WHERE id=?",
        (quality_rating, quality_notes, session_id),
    )
    await db.commit()
