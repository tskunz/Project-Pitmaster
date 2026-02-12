"""9-state cook state machine with transition rules.

States: SETUP → PREHEAT → EARLY_COOK → PRE_STALL → STALL →
        POST_STALL → APPROACHING_TARGET → REST → DONE

Transitions are driven by probe temperature readings and time.
"""

from ..models.enums import CookState
from ..models.dataclasses import CookSession, ProbeReading
from ..simulation.stall_model import detect_stall_override, compute_slope

# Temperature thresholds for state transitions
PREHEAT_SMOKER_TEMP_THRESHOLD = 200.0  # smoker must be above this
EARLY_COOK_TEMP = 100.0  # meat above this → EARLY_COOK
PRE_STALL_TEMP = 130.0   # approaching stall zone
STALL_ENTRY_TEMP = 140.0
STALL_EXIT_TEMP = 175.0  # confirmed past stall
APPROACHING_THRESHOLD_DELTA = 10.0  # within X°F of target


# Valid transitions
TRANSITIONS: dict[CookState, list[CookState]] = {
    CookState.SETUP: [CookState.PREHEAT],
    CookState.PREHEAT: [CookState.EARLY_COOK],
    CookState.EARLY_COOK: [CookState.PRE_STALL],
    CookState.PRE_STALL: [CookState.STALL, CookState.POST_STALL],
    CookState.STALL: [CookState.POST_STALL],
    CookState.POST_STALL: [CookState.APPROACHING_TARGET],
    CookState.APPROACHING_TARGET: [CookState.REST, CookState.DONE],
    CookState.REST: [CookState.DONE],
    CookState.DONE: [],
}


class CookStateMachine:
    """Manages state transitions for a cook session."""

    def __init__(self, session: CookSession):
        self.session = session

    @property
    def state(self) -> CookState:
        return self.session.current_state

    def advance(self, reading: ProbeReading) -> CookState:
        """Evaluate and potentially advance the cook state based on a new reading.

        Args:
            reading: The latest probe reading.

        Returns:
            The (possibly new) current state.
        """
        current = self.session.current_state
        temp = reading.temp_f
        target = self.session.target_temp_f

        new_state = current

        if current == CookState.SETUP:
            # Transition to PREHEAT once session is created
            new_state = CookState.PREHEAT

        elif current == CookState.PREHEAT:
            if temp >= EARLY_COOK_TEMP:
                new_state = CookState.EARLY_COOK

        elif current == CookState.EARLY_COOK:
            if temp >= PRE_STALL_TEMP:
                new_state = CookState.PRE_STALL

        elif current == CookState.PRE_STALL:
            # Check for stall entry
            if temp >= STALL_ENTRY_TEMP:
                # Check slope-based override
                slopes = self.session.stall.slope_history
                if detect_stall_override(slopes, temp):
                    new_state = CookState.STALL
                    self.session.stall.in_stall = True
                    self.session.stall.stall_start_temp_f = temp
                    self.session.stall.stall_start_minutes = reading.elapsed_minutes
                elif temp >= STALL_EXIT_TEMP:
                    # Skipped stall (e.g., wrapped early)
                    new_state = CookState.POST_STALL

        elif current == CookState.STALL:
            self.session.stall.stall_duration_minutes = (
                reading.elapsed_minutes - (self.session.stall.stall_start_minutes or 0)
            )
            if temp >= STALL_EXIT_TEMP:
                new_state = CookState.POST_STALL
                self.session.stall.in_stall = False

        elif current == CookState.POST_STALL:
            if temp >= target - APPROACHING_THRESHOLD_DELTA:
                new_state = CookState.APPROACHING_TARGET

        elif current == CookState.APPROACHING_TARGET:
            if temp >= target:
                new_state = CookState.DONE

        elif current == CookState.REST:
            # REST → DONE is typically manual
            pass

        # Validate transition
        if new_state != current:
            if new_state in TRANSITIONS.get(current, []):
                self.session.current_state = new_state
            else:
                # Invalid transition — stay in current state
                new_state = current

        # Update slope history
        temps = [r.temp_f for r in self.session.readings]
        if len(temps) >= 2:
            slope = compute_slope(temps[-2:])
            self.session.stall.slope_history.append(slope)

        return self.session.current_state

    def force_state(self, state: CookState) -> None:
        """Force a state transition (for REST and DONE)."""
        self.session.current_state = state

    def finish(self) -> CookState:
        """Mark the cook as done."""
        self.session.current_state = CookState.DONE
        self.session.is_finished = True
        return CookState.DONE
