"""Stall model: logistic hazard function + slope detection override.

The stall is modeled as a probabilistic event gated by temperature (140-185°F).
A logistic hazard function determines stall probability at each temperature.
A slope detection override triggers stall state when observed temp slope
falls below 0.02°F/min for 10+ consecutive minutes.
"""

import numpy as np


# Logistic hazard function coefficients (from spec)
BETA_0 = -8.0   # intercept
BETA_TEMP = 0.05  # temperature coefficient
TEMP_MIDPOINT = 160.0  # inflection point

# Stall detection thresholds
SLOPE_THRESHOLD = 0.02  # °F/min — below this is "stalled"
MIN_STALL_DURATION_MIN = 10  # consecutive minutes below threshold to confirm
STALL_TEMP_LOW = 140.0
STALL_TEMP_HIGH = 185.0


def stall_probability(temp_f: float) -> float:
    """Compute the probability that the meat is in a stall at given temp.

    Uses a logistic function gated to the 140-185°F stall zone.

    Returns:
        Probability between 0 and 1.
    """
    if temp_f < STALL_TEMP_LOW or temp_f > STALL_TEMP_HIGH:
        return 0.0

    z = BETA_0 + BETA_TEMP * (temp_f - STALL_TEMP_LOW)
    # Logistic with midpoint at ~160°F
    logit = -4.0 + 0.2 * (temp_f - STALL_TEMP_LOW)
    return 1.0 / (1.0 + np.exp(-logit))


def detect_stall_override(
    slope_history: list[float],
    current_temp_f: float,
) -> bool:
    """Determine if stall should be forced based on observed slope.

    Triggers when slope < 0.02°F/min for 10+ consecutive minutes
    and temperature is in the stall zone.

    Args:
        slope_history: Recent temperature slopes (°F/min), newest last.
        current_temp_f: Current probe temperature.

    Returns:
        True if stall should be declared via override.
    """
    if current_temp_f < STALL_TEMP_LOW or current_temp_f > STALL_TEMP_HIGH:
        return False

    if len(slope_history) < MIN_STALL_DURATION_MIN:
        return False

    recent = slope_history[-MIN_STALL_DURATION_MIN:]
    return all(s < SLOPE_THRESHOLD for s in recent)


def compute_slope(temps: list[float], dt_minutes: float = 1.0) -> float:
    """Compute the current temperature slope from recent readings.

    Args:
        temps: Recent temperature readings (at least 2).
        dt_minutes: Time between readings.

    Returns:
        Slope in °F/min. Returns 0.0 if insufficient data.
    """
    if len(temps) < 2:
        return 0.0
    return (temps[-1] - temps[-2]) / dt_minutes


def compute_slope_history(
    temps: list[float], window: int = 15, dt_minutes: float = 1.0
) -> list[float]:
    """Compute slope history over a sliding window.

    Args:
        temps: Full temperature history.
        window: Number of recent readings to compute slopes for.
        dt_minutes: Time between readings.

    Returns:
        List of slopes (°F/min) for the last `window` intervals.
    """
    if len(temps) < 2:
        return []

    start = max(0, len(temps) - window - 1)
    slopes = []
    for i in range(start + 1, len(temps)):
        slopes.append((temps[i] - temps[i - 1]) / dt_minutes)
    return slopes
