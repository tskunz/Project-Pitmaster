"""Report API endpoint."""

from fastapi import APIRouter, HTTPException

from ..models.schemas import ReportResponse
from ..services import cook_session_service as svc

router = APIRouter(prefix="/api/v1/report", tags=["report"])


@router.get("/{session_id}", response_model=ReportResponse)
async def get_report(session_id: str):
    """Get post-cook report."""
    report = await svc.get_report(session_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found or cook not finished")

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
