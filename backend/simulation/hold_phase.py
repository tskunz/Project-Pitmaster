"""Hold/rest phase calculator using Newton's Law of Cooling.

After pulling meat off the smoker, temperature continues to rise
(carryover cooking) then decays toward ambient. This module estimates:
- Peak carryover temperature
- Time to reach serving temperature
- Recommended rest duration
"""

import numpy as np
from ..models.dataclasses import HoldPhaseResult


# Carryover cooking: meat typically rises 5-10°F after pulling
CARRYOVER_RISE_F = 7.0

# Newton's Law of Cooling decay constant (1/min)
# Typical for wrapped brisket in a cooler
COOLING_CONSTANT = 0.005

# Ambient temperature during rest (insulated cooler)
REST_AMBIENT_F = 150.0

# Minimum recommended rest (minutes)
MIN_REST_MINUTES = 30.0

# Serving temperature target
SERVING_TEMP_F = 165.0


def calculate_hold_phase(
    pull_temp_f: float,
    ambient_temp_f: float = REST_AMBIENT_F,
    serving_temp_f: float = SERVING_TEMP_F,
    is_wrapped: bool = True,
) -> HoldPhaseResult:
    """Calculate rest phase behavior using Newton's Law of Cooling.

    T(t) = T_ambient + (T_peak - T_ambient) * exp(-k * t)

    Args:
        pull_temp_f: Temperature when meat was pulled from smoker.
        ambient_temp_f: Rest environment temperature (cooler/counter).
        serving_temp_f: Target serving temperature.
        is_wrapped: Whether meat is wrapped (affects cooling rate).

    Returns:
        HoldPhaseResult with carryover peak, time estimates.
    """
    # Carryover rise
    peak = pull_temp_f + CARRYOVER_RISE_F

    # Cooling rate — wrapped meat cools slower
    k = COOLING_CONSTANT
    if not is_wrapped:
        k *= 2.0  # unwrapped cools faster

    # Time to reach serving temp from peak
    if peak <= serving_temp_f:
        time_to_serving = 0.0
    elif serving_temp_f <= ambient_temp_f:
        time_to_serving = float("inf")
    else:
        # T(t) = T_amb + (T_peak - T_amb) * exp(-k * t)
        # Solve for t: t = -ln((T_serve - T_amb) / (T_peak - T_amb)) / k
        ratio = (serving_temp_f - ambient_temp_f) / (peak - ambient_temp_f)
        if ratio <= 0 or ratio >= 1:
            time_to_serving = 0.0
        else:
            time_to_serving = -np.log(ratio) / k

    recommended_rest = max(MIN_REST_MINUTES, min(time_to_serving, 120.0))

    return HoldPhaseResult(
        carryover_peak_f=round(peak, 1),
        time_to_serving_temp_minutes=round(time_to_serving, 1),
        recommended_rest_minutes=round(recommended_rest, 1),
    )
