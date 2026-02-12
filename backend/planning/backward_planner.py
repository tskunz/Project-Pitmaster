"""Backward planner: dinner_time → fire-start time.

Given a target dinner time, works backward using the P90 (conservative)
estimate to determine when to start the fire, put the meat on, etc.
"""

from datetime import datetime, timedelta
from ..models.dataclasses import BackwardPlan, PredictionResult


# Default timing assumptions
DEFAULT_PREHEAT_MINUTES = 30.0
DEFAULT_REST_MINUTES = 30.0


def compute_backward_plan(
    dinner_time: datetime,
    prediction: PredictionResult,
    preheat_minutes: float = DEFAULT_PREHEAT_MINUTES,
    rest_minutes: float = DEFAULT_REST_MINUTES,
) -> BackwardPlan:
    """Compute backward plan from dinner time using P90 estimate.

    Timeline: fire_start → preheat → meat_on → cook (P90) → rest → dinner

    Args:
        dinner_time: When you want to eat.
        prediction: MC prediction with P10/P50/P90.
        preheat_minutes: Time to preheat smoker.
        rest_minutes: Rest period after cook.

    Returns:
        BackwardPlan with all milestone times.
    """
    cook_minutes_p90 = prediction.p90_minutes

    # Work backward from dinner
    # dinner = meat_on + cook_time + rest
    total_before_dinner = cook_minutes_p90 + rest_minutes
    meat_on_time = dinner_time - timedelta(minutes=total_before_dinner)
    fire_start_time = meat_on_time - timedelta(minutes=preheat_minutes)

    return BackwardPlan(
        dinner_time=dinner_time,
        estimated_cook_minutes_p90=round(cook_minutes_p90, 1),
        rest_minutes=rest_minutes,
        fire_start_time=fire_start_time,
        meat_on_time=meat_on_time,
        preheat_minutes=preheat_minutes,
    )
