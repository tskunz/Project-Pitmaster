"""Equipment profiles service.

5 presets (offset, pellet, kamado, WSM, custom) with temp variance
and recovery parameters.
"""

from ..models.enums import EquipmentType
from ..models.dataclasses import EquipmentProfile


EQUIPMENT_PRESETS: dict[EquipmentType, EquipmentProfile] = {
    EquipmentType.OFFSET: EquipmentProfile(
        equipment_type=EquipmentType.OFFSET,
        name="Offset Smoker",
        temp_variance=15.0,
        recovery_time_min=8.0,
        temp_drop_on_lid_open=25.0,
        insulation_factor=0.8,
    ),
    EquipmentType.PELLET: EquipmentProfile(
        equipment_type=EquipmentType.PELLET,
        name="Pellet Grill",
        temp_variance=5.0,
        recovery_time_min=3.0,
        temp_drop_on_lid_open=15.0,
        insulation_factor=1.0,
    ),
    EquipmentType.KAMADO: EquipmentProfile(
        equipment_type=EquipmentType.KAMADO,
        name="Kamado (Big Green Egg / Kamado Joe)",
        temp_variance=8.0,
        recovery_time_min=5.0,
        temp_drop_on_lid_open=20.0,
        insulation_factor=1.3,
    ),
    EquipmentType.WSM: EquipmentProfile(
        equipment_type=EquipmentType.WSM,
        name="Weber Smokey Mountain",
        temp_variance=10.0,
        recovery_time_min=6.0,
        temp_drop_on_lid_open=20.0,
        insulation_factor=1.0,
    ),
    EquipmentType.CUSTOM: EquipmentProfile(
        equipment_type=EquipmentType.CUSTOM,
        name="Custom / Other",
        temp_variance=12.0,
        recovery_time_min=5.0,
        temp_drop_on_lid_open=20.0,
        insulation_factor=1.0,
    ),
}


def get_all_presets() -> list[EquipmentProfile]:
    """Return all equipment presets."""
    return list(EQUIPMENT_PRESETS.values())


def get_preset(equipment_type: EquipmentType) -> EquipmentProfile:
    """Get a specific equipment preset."""
    return EQUIPMENT_PRESETS.get(equipment_type, EQUIPMENT_PRESETS[EquipmentType.CUSTOM])
