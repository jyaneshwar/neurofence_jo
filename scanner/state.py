"""
NeuroFence - Scan State Management

Defines the lifecycle states used by the NeuroFence
security scanning workflow.
"""

from enum import Enum


class ScanState(str, Enum):
    """
    Represents the current state of a security scan.
    """

    IDLE = "idle"

    LOADING = "loading"

    SCANNING = "scanning"

    ANALYZING = "analyzing"

    COMPLETED = "completed"

    ERROR = "error"

    CANCELLED = "cancelled"


class ScanStateManager:
    """
    Maintains the current scan state and validates
    state transitions.
    """

    VALID_TRANSITIONS = {
        ScanState.IDLE: {
            ScanState.LOADING,
        },

        ScanState.LOADING: {
            ScanState.SCANNING,
            ScanState.ERROR,
            ScanState.CANCELLED,
        },

        ScanState.SCANNING: {
            ScanState.ANALYZING,
            ScanState.ERROR,
            ScanState.CANCELLED,
        },

        ScanState.ANALYZING: {
            ScanState.COMPLETED,
            ScanState.ERROR,
            ScanState.CANCELLED,
        },

        ScanState.COMPLETED: {
            ScanState.IDLE,
        },

        ScanState.ERROR: {
            ScanState.IDLE,
        },

        ScanState.CANCELLED: {
            ScanState.IDLE,
        },
    }

    def __init__(self):
        self._state = ScanState.IDLE

    @property
    def state(self) -> ScanState:
        """
        Return the current scan state.
        """

        return self._state

    def transition_to(
        self,
        new_state: ScanState,
    ) -> None:
        """
        Move the scanner to a new state.

        Raises
        ------
        ValueError
            If the requested transition is invalid.
        """

        if new_state == self._state:
            return

        allowed_states = self.VALID_TRANSITIONS.get(
            self._state,
            set(),
        )

        if new_state not in allowed_states:

            raise ValueError(
                f"Invalid scan state transition: "
                f"{self._state.value} -> {new_state.value}"
            )

        self._state = new_state

    def reset(self) -> None:
        """
        Return the scanner to the IDLE state.
        """

        if self._state == ScanState.IDLE:
            return

        self._state = ScanState.IDLE