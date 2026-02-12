"""Tests for the 9-state cook state machine."""

import pytest
from datetime import datetime

from backend.state_machine.cook_states import CookStateMachine
from backend.models.enums import CookState, CutType, EquipmentType, MeatCategory
from backend.models.dataclasses import CookSession, ProbeReading


def _make_session(state: CookState = CookState.SETUP) -> CookSession:
    return CookSession(
        id="test-sm",
        meat_category=MeatCategory.BEEF,
        cut_type=CutType.BRISKET,
        weight_lbs=10.0,
        thickness_inches=5.0,
        equipment_type=EquipmentType.OFFSET,
        smoker_temp_f=250.0,
        target_temp_f=203.0,
        current_state=state,
    )


def _reading(temp: float, elapsed: float = 0.0) -> ProbeReading:
    return ProbeReading(temp_f=temp, elapsed_minutes=elapsed)


def test_setup_to_preheat():
    session = _make_session(CookState.SETUP)
    sm = CookStateMachine(session)
    result = sm.advance(_reading(40.0))
    assert result == CookState.PREHEAT


def test_preheat_to_early_cook():
    session = _make_session(CookState.PREHEAT)
    sm = CookStateMachine(session)
    result = sm.advance(_reading(105.0))
    assert result == CookState.EARLY_COOK


def test_early_cook_to_pre_stall():
    session = _make_session(CookState.EARLY_COOK)
    sm = CookStateMachine(session)
    result = sm.advance(_reading(135.0))
    assert result == CookState.PRE_STALL


def test_stall_to_post_stall():
    session = _make_session(CookState.STALL)
    session.stall.in_stall = True
    session.stall.stall_start_minutes = 0
    sm = CookStateMachine(session)
    result = sm.advance(_reading(180.0, elapsed=120))
    assert result == CookState.POST_STALL


def test_post_stall_to_approaching():
    session = _make_session(CookState.POST_STALL)
    sm = CookStateMachine(session)
    result = sm.advance(_reading(195.0))
    assert result == CookState.APPROACHING_TARGET


def test_approaching_to_done():
    session = _make_session(CookState.APPROACHING_TARGET)
    sm = CookStateMachine(session)
    result = sm.advance(_reading(203.0))
    assert result == CookState.DONE


def test_full_walkthrough():
    """Drive a session through SETUP → DONE with synthetic readings."""
    session = _make_session(CookState.SETUP)
    sm = CookStateMachine(session)

    # SETUP → PREHEAT
    sm.advance(_reading(40.0, 0))
    assert session.current_state == CookState.PREHEAT

    # PREHEAT → EARLY_COOK
    session.readings.append(_reading(40.0, 0))
    sm.advance(_reading(105.0, 30))
    assert session.current_state == CookState.EARLY_COOK

    # EARLY_COOK → PRE_STALL
    session.readings.append(_reading(105.0, 30))
    sm.advance(_reading(135.0, 120))
    assert session.current_state == CookState.PRE_STALL

    # PRE_STALL → POST_STALL (skipping stall — high enough temp)
    session.readings.append(_reading(135.0, 120))
    sm.advance(_reading(180.0, 300))
    assert session.current_state == CookState.POST_STALL

    # POST_STALL → APPROACHING_TARGET
    session.readings.append(_reading(180.0, 300))
    sm.advance(_reading(195.0, 400))
    assert session.current_state == CookState.APPROACHING_TARGET

    # APPROACHING_TARGET → DONE
    session.readings.append(_reading(195.0, 400))
    sm.advance(_reading(204.0, 500))
    assert session.current_state == CookState.DONE


def test_finish_method():
    session = _make_session(CookState.APPROACHING_TARGET)
    sm = CookStateMachine(session)
    sm.finish()
    assert session.current_state == CookState.DONE
    assert session.is_finished is True
