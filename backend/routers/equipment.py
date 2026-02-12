"""Equipment presets API endpoint."""

from fastapi import APIRouter

from ..models.schemas import EquipmentPresetResponse
from ..services.equipment_service import get_all_presets

router = APIRouter(prefix="/api/v1/equipment", tags=["equipment"])


@router.get("/presets", response_model=list[EquipmentPresetResponse])
async def list_presets():
    """List all equipment profiles."""
    presets = get_all_presets()
    return [
        EquipmentPresetResponse(
            equipment_type=p.equipment_type,
            name=p.name,
            temp_variance=p.temp_variance,
            recovery_time_min=p.recovery_time_min,
            temp_drop_on_lid_open=p.temp_drop_on_lid_open,
            insulation_factor=p.insulation_factor,
        )
        for p in presets
    ]
