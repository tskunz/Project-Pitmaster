"""Tests for the physics kernel."""

import numpy as np
import pytest

from backend.simulation.physics import solve_1d_heat, THERMAL_DIFFUSIVITY
from backend.simulation.altitude import boiling_point_at_altitude
from backend.models.enums import CutType, WrapType


def test_boiling_point_sea_level():
    assert boiling_point_at_altitude(0) == 212.0


def test_boiling_point_denver():
    # Denver ~5280 ft → 212 - 1.5*5.28 = 204.08
    bp = boiling_point_at_altitude(5280)
    assert 203.5 < bp < 205.0


def test_boiling_point_high_altitude():
    bp = boiling_point_at_altitude(10000)
    assert bp == pytest.approx(197.0, abs=0.1)


def test_solve_heat_reaches_target():
    """A basic cook should eventually reach target temperature."""
    temps, finish = solve_1d_heat(
        cut_type=CutType.BRISKET,
        thickness_inches=5.0,
        smoker_temp_f=250.0,
        initial_temp_f=40.0,
        target_temp_f=203.0,
        dt_minutes=1.0,
        max_minutes=1800,
    )
    assert np.isfinite(finish), "Brisket should finish within 1800 minutes"
    assert finish > 60, "Brisket should take more than 1 hour"


def test_thinner_cooks_faster():
    """Thinner meat should finish faster than thicker meat."""
    _, finish_thin = solve_1d_heat(
        cut_type=CutType.PORK_RIBS,
        thickness_inches=1.5,
        smoker_temp_f=250.0,
        initial_temp_f=40.0,
        target_temp_f=195.0,
        max_minutes=1800,
    )
    _, finish_thick = solve_1d_heat(
        cut_type=CutType.PORK_RIBS,
        thickness_inches=3.0,
        smoker_temp_f=250.0,
        initial_temp_f=40.0,
        target_temp_f=195.0,
        max_minutes=1800,
    )
    assert finish_thin < finish_thick


def test_higher_smoker_temp_cooks_faster():
    """Higher smoker temp should result in faster cook."""
    _, finish_low = solve_1d_heat(
        cut_type=CutType.BRISKET,
        thickness_inches=5.0,
        smoker_temp_f=225.0,
        initial_temp_f=40.0,
        target_temp_f=203.0,
        max_minutes=1800,
    )
    _, finish_high = solve_1d_heat(
        cut_type=CutType.BRISKET,
        thickness_inches=5.0,
        smoker_temp_f=275.0,
        initial_temp_f=40.0,
        target_temp_f=203.0,
        max_minutes=1800,
    )
    assert finish_high < finish_low


def test_wrap_reduces_cook_time():
    """Wrapping in foil should reduce cook time."""
    _, finish_unwrapped = solve_1d_heat(
        cut_type=CutType.BRISKET,
        thickness_inches=5.0,
        smoker_temp_f=250.0,
        initial_temp_f=40.0,
        target_temp_f=203.0,
        wrap_type=WrapType.NONE,
        max_minutes=1800,
    )
    _, finish_wrapped = solve_1d_heat(
        cut_type=CutType.BRISKET,
        thickness_inches=5.0,
        smoker_temp_f=250.0,
        initial_temp_f=40.0,
        target_temp_f=203.0,
        wrap_type=WrapType.FOIL,
        max_minutes=1800,
    )
    assert finish_wrapped < finish_unwrapped


def test_temp_history_is_monotonically_increasing_roughly():
    """Temperature should generally increase over the cook."""
    temps, _ = solve_1d_heat(
        cut_type=CutType.CHICKEN_WHOLE,
        thickness_inches=4.0,
        smoker_temp_f=300.0,
        initial_temp_f=40.0,
        target_temp_f=165.0,
        max_minutes=600,
    )
    # Check that the final temp is higher than initial
    valid = temps[temps > 0]
    if len(valid) > 10:
        assert valid[-1] > valid[0]
