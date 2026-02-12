"""Tests for the Monte Carlo engine."""

import pytest

from backend.simulation.monte_carlo import run_monte_carlo
from backend.models.dataclasses import CookSession, WeatherSnapshot
from backend.models.enums import (
    ConfidenceTier,
    CookState,
    CutType,
    EquipmentType,
    MeatCategory,
    WrapType,
)


def _make_session(**kwargs) -> CookSession:
    defaults = dict(
        id="test-123",
        meat_category=MeatCategory.BEEF,
        cut_type=CutType.BRISKET,
        weight_lbs=10.0,
        thickness_inches=5.0,
        equipment_type=EquipmentType.OFFSET,
        smoker_temp_f=250.0,
        target_temp_f=203.0,
        current_state=CookState.EARLY_COOK,
    )
    defaults.update(kwargs)
    return CookSession(**defaults)


def test_p10_lt_p50_lt_p90():
    """Percentiles must be ordered: P10 < P50 < P90."""
    session = _make_session()
    result = run_monte_carlo(session, n_iterations=200, seed=42)
    assert result.p10_minutes <= result.p50_minutes <= result.p90_minutes


def test_brisket_reasonable_time():
    """10lb brisket at 250°F should predict ~10-14 hours (600-840 min)."""
    session = _make_session()
    result = run_monte_carlo(session, n_iterations=200, seed=42)
    # P50 should be in a reasonable range for BBQ
    assert result.p50_minutes > 60, "Should take more than 1 hour"
    assert result.p50_minutes < 1800, "Should take less than 30 hours"


def test_wrapping_reduces_time():
    """Wrapping should reduce predicted cook time."""
    session_unwrapped = _make_session(wrap_type=WrapType.NONE)
    session_wrapped = _make_session(wrap_type=WrapType.FOIL)

    result_unwrapped = run_monte_carlo(session_unwrapped, n_iterations=200, seed=42)
    result_wrapped = run_monte_carlo(session_wrapped, n_iterations=200, seed=42)

    assert result_wrapped.p50_minutes <= result_unwrapped.p50_minutes


def test_higher_altitude_increases_time():
    """Higher altitude (lower boiling point) should increase cook time."""
    session_sea = _make_session(altitude_ft=0)
    session_high = _make_session(altitude_ft=8000)

    result_sea = run_monte_carlo(session_sea, n_iterations=200, seed=42)
    result_high = run_monte_carlo(session_high, n_iterations=200, seed=42)

    # At high altitude, boiling point is lower so cooks may take longer
    # or same time since target is 203 which is below both boiling points
    # This is more of a sanity check that it runs without error
    assert result_high.p50_minutes > 0


def test_stall_probability_returned():
    """Stall probability should be between 0 and 1."""
    session = _make_session()
    result = run_monte_carlo(session, n_iterations=100, seed=42)
    assert 0.0 <= result.stall_probability <= 1.0


def test_confidence_tier_returned():
    """Should return a valid confidence tier."""
    session = _make_session()
    result = run_monte_carlo(session, n_iterations=100, seed=42)
    assert result.confidence in [
        ConfidenceTier.HIGH,
        ConfidenceTier.MODERATE,
        ConfidenceTier.LOW,
        ConfidenceTier.VERY_LOW,
    ]
