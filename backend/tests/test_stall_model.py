"""Tests for the stall model."""

import pytest

from backend.simulation.stall_model import (
    stall_probability,
    detect_stall_override,
    compute_slope,
    compute_slope_history,
)


def test_stall_probability_below_zone():
    assert stall_probability(130.0) == 0.0


def test_stall_probability_above_zone():
    assert stall_probability(190.0) == 0.0


def test_stall_probability_in_zone():
    prob = stall_probability(160.0)
    assert 0.0 < prob <= 1.0


def test_stall_probability_peaks_near_middle():
    p_low = stall_probability(145.0)
    p_mid = stall_probability(165.0)
    p_high = stall_probability(180.0)
    # Should be higher in the middle of the zone
    assert p_mid > p_low


def test_detect_stall_override_insufficient_data():
    assert detect_stall_override([0.01, 0.01], 160.0) is False


def test_detect_stall_override_triggers():
    # 10+ consecutive readings with slope < 0.02
    slopes = [0.01] * 15
    assert detect_stall_override(slopes, 160.0) is True


def test_detect_stall_override_not_in_zone():
    slopes = [0.01] * 15
    assert detect_stall_override(slopes, 120.0) is False


def test_detect_stall_override_above_threshold():
    slopes = [0.05] * 15
    assert detect_stall_override(slopes, 160.0) is False


def test_compute_slope():
    assert compute_slope([150.0, 151.0]) == pytest.approx(1.0)
    assert compute_slope([150.0, 150.0]) == pytest.approx(0.0)
    assert compute_slope([]) == 0.0
    assert compute_slope([150.0]) == 0.0


def test_compute_slope_history():
    temps = [140, 141, 142, 143, 143.5, 143.8, 144.0]
    slopes = compute_slope_history(temps, window=5)
    assert len(slopes) > 0
    # Slopes should decrease as temp plateaus
    assert slopes[-1] < slopes[0]
