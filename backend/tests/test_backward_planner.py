"""Tests for the backward planner."""

import pytest
from datetime import datetime, timedelta

from backend.planning.backward_planner import compute_backward_plan
from backend.models.dataclasses import PredictionResult
from backend.models.enums import ConfidenceTier, CookState


def test_backward_plan_ordering():
    """fire_start < meat_on < dinner_time."""
    dinner = datetime(2024, 7, 4, 18, 0)  # July 4th at 6 PM
    prediction = PredictionResult(
        p10_minutes=480,
        p50_minutes=600,
        p90_minutes=720,  # 12 hours
        confidence=ConfidenceTier.MODERATE,
        current_state=CookState.PREHEAT,
    )

    plan = compute_backward_plan(dinner, prediction)
    assert plan.fire_start_time < plan.meat_on_time < plan.dinner_time


def test_backward_plan_uses_p90():
    """Plan should use P90 (conservative) estimate."""
    dinner = datetime(2024, 7, 4, 18, 0)
    prediction = PredictionResult(
        p10_minutes=480,
        p50_minutes=600,
        p90_minutes=720,
    )

    plan = compute_backward_plan(dinner, prediction)
    assert plan.estimated_cook_minutes_p90 == 720.0


def test_backward_plan_math():
    """Verify the math: dinner = meat_on + cook_p90 + rest."""
    dinner = datetime(2024, 12, 25, 17, 0)
    prediction = PredictionResult(p90_minutes=600)

    plan = compute_backward_plan(dinner, prediction, preheat_minutes=30, rest_minutes=30)

    expected_meat_on = dinner - timedelta(minutes=600 + 30)
    expected_fire_start = expected_meat_on - timedelta(minutes=30)

    assert abs((plan.meat_on_time - expected_meat_on).total_seconds()) < 1
    assert abs((plan.fire_start_time - expected_fire_start).total_seconds()) < 1


def test_backward_plan_with_short_cook():
    """Chicken — short cook time should still produce valid plan."""
    dinner = datetime(2024, 8, 1, 18, 0)
    prediction = PredictionResult(p90_minutes=120)

    plan = compute_backward_plan(dinner, prediction)
    assert plan.fire_start_time < dinner
    # For a 2-hour cook, fire start should be ~3 hours before dinner
    diff = (dinner - plan.fire_start_time).total_seconds() / 60
    assert 150 < diff < 200  # 120 cook + 30 rest + 30 preheat = 180 min
