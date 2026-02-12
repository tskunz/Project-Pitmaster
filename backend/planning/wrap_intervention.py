"""Wrap intervention logic.

Wrapping the meat adjusts the evaporative cooling coefficient, which
affects stall duration. This module provides:
- Wrap type coefficients and their effects
- Tradeoff descriptions for user display
- Model adjustment when wrap is applied
"""

from ..models.enums import WrapType


# Evaporative cooling reduction by wrap type
WRAP_COEFFICIENTS: dict[WrapType, float] = {
    WrapType.NONE: 0.0,
    WrapType.FOIL: 0.95,          # ~95% reduction — fastest through stall
    WrapType.BUTCHER_PAPER: 0.60,  # ~60% reduction — good bark retention
    WrapType.FOIL_BOAT: 0.45,     # ~45% reduction — moderate protection
}

# User-facing tradeoff descriptions
WRAP_TRADEOFFS: dict[WrapType, dict[str, str]] = {
    WrapType.NONE: {
        "title": "No Wrap",
        "pros": "Maximum bark development, most traditional flavor",
        "cons": "Longest stall duration, most variable cook time",
        "effect": "No change to cook time estimate",
    },
    WrapType.FOIL: {
        "title": "Aluminum Foil (Texas Crutch)",
        "pros": "Fastest through stall, most moisture retention",
        "cons": "Softer bark, can get mushy texture",
        "effect": "Reduces remaining cook time by ~30-40%",
    },
    WrapType.BUTCHER_PAPER: {
        "title": "Butcher Paper",
        "pros": "Good bark retention, breathable, balanced moisture",
        "cons": "Slower than foil, paper can tear",
        "effect": "Reduces remaining cook time by ~15-25%",
    },
    WrapType.FOIL_BOAT: {
        "title": "Foil Boat",
        "pros": "Protects bottom, collects juices, decent bark on top",
        "cons": "Less stall protection than full wrap",
        "effect": "Reduces remaining cook time by ~10-15%",
    },
}


def get_wrap_tradeoff(wrap_type: WrapType) -> dict[str, str]:
    """Get user-facing tradeoff description for a wrap type."""
    return WRAP_TRADEOFFS.get(wrap_type, WRAP_TRADEOFFS[WrapType.NONE])


def get_evap_reduction(wrap_type: WrapType) -> float:
    """Get the evaporative cooling reduction factor for a wrap type."""
    return WRAP_COEFFICIENTS.get(wrap_type, 0.0)


def should_suggest_wrap(
    current_temp_f: float,
    stall_duration_minutes: float,
    is_wrapped: bool,
) -> bool:
    """Determine if we should suggest wrapping to the user.

    Suggests wrap when:
    - Meat is in stall zone (150-175°F)
    - Stall has lasted > 30 minutes
    - Not already wrapped

    Args:
        current_temp_f: Current probe temperature.
        stall_duration_minutes: How long the stall has lasted.
        is_wrapped: Whether meat is already wrapped.

    Returns:
        True if wrap should be suggested.
    """
    if is_wrapped:
        return False
    if current_temp_f < 150.0 or current_temp_f > 175.0:
        return False
    if stall_duration_minutes < 30.0:
        return False
    return True
