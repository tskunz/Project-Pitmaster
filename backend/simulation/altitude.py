"""Altitude correction for boiling point."""


def boiling_point_at_altitude(altitude_ft: float) -> float:
    """Calculate boiling point of water at a given altitude.

    Formula: T_bp = 212 - (1.5 × altitude_ft / 1000)
    """
    return 212.0 - (1.5 * altitude_ft / 1000.0)
