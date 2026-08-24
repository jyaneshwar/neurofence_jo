"""
NeuroFence - Security Scan Workflow

Coordinates the lifecycle of a security scan.

This module does not contain the actual threat-detection
implementation. It provides the orchestration layer that
future scanner components can plug into.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, Optional

from scanner.state import (
    ScanState,
    ScanStateManager,
)


@dataclass
class ScanContext:
    """
    Stores information associated with one scan.
    """

    scan_id: str

    model_path: str

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    state: ScanState = ScanState.IDLE

    progress: int = 0

    error: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


class ScanWorkflow:
    """
    Controls the lifecycle of a NeuroFence scan.
    """

    def __init__(
        self,
        scan_id: str,
        model_path: str,
    ):
        self.state_manager = ScanStateManager()

        self.context = ScanContext(
            scan_id=scan_id,
            model_path=model_path,
        )

        self._cancel_requested = False

        self._listeners = []

    # ----------------------------------------------------------
    # LISTENERS
    # ----------------------------------------------------------

    def add_listener(
        self,
        listener: Callable[[ScanState], None],
    ) -> None:
        """
        Register a callback that receives state updates.
        """

        if listener not in self._listeners:

            self._listeners.append(
                listener
            )

    def remove_listener(
        self,
        listener: Callable[[ScanState], None],
    ) -> None:
        """
        Remove a previously registered listener.
        """

        if listener in self._listeners:

            self._listeners.remove(
                listener
            )

    def _notify_state_change(self) -> None:

        current_state = self.state_manager.state

        self.context.state = current_state

        for listener in list(
            self._listeners
        ):

            listener(
                current_state
            )

    # ----------------------------------------------------------
    # STATE
    # ----------------------------------------------------------

    @property
    def state(self) -> ScanState:

        return self.state_manager.state

    @property
    def progress(self) -> int:

        return self.context.progress

    # ----------------------------------------------------------
    # START
    # ----------------------------------------------------------

    def start(self) -> None:
        """
        Start a new security scan.
        """

        if self.state != ScanState.IDLE:

            raise RuntimeError(
                "A scan can only be started "
                "from the IDLE state."
            )

        self._cancel_requested = False

        self.context.started_at = datetime.now()

        self.context.completed_at = None

        self.context.error = None

        self.context.progress = 0

        self._transition(
            ScanState.LOADING
        )

    # ----------------------------------------------------------
    # LOADING
    # ----------------------------------------------------------

    def begin_scanning(self) -> None:
        """
        Indicate that model loading has completed
        and security scanning can begin.
        """

        self._ensure_not_cancelled()

        self._transition(
            ScanState.SCANNING
        )

    # ----------------------------------------------------------
    # ANALYSIS
    # ----------------------------------------------------------

    def begin_analysis(self) -> None:
        """
        Move from scanning into activation/threat analysis.
        """

        self._ensure_not_cancelled()

        self._transition(
            ScanState.ANALYZING
        )

    # ----------------------------------------------------------
    # PROGRESS
    # ----------------------------------------------------------

    def update_progress(
        self,
        progress: int,
    ) -> None:
        """
        Update scan progress.

        Progress is always constrained to 0-100.
        """

        if not 0 <= progress <= 100:

            raise ValueError(
                "Progress must be between 0 and 100."
            )

        self.context.progress = progress

    # ----------------------------------------------------------
    # COMPLETE
    # ----------------------------------------------------------

    def complete(
        self,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Mark the scan as completed.
        """

        self._ensure_not_cancelled()

        if self.state != ScanState.ANALYZING:

            raise RuntimeError(
                "A scan must be in ANALYZING state "
                "before it can be completed."
            )

        if metadata:

            self.context.metadata.update(
                metadata
            )

        self.context.progress = 100

        self.context.completed_at = datetime.now()

        self._transition(
            ScanState.COMPLETED
        )

    # ----------------------------------------------------------
    # ERROR
    # ----------------------------------------------------------

    def fail(
        self,
        error_message: str,
    ) -> None:
        """
        Mark the current scan as failed.
        """

        self.context.error = error_message

        self.context.completed_at = datetime.now()

        self._transition(
            ScanState.ERROR
        )

    # ----------------------------------------------------------
    # CANCEL
    # ----------------------------------------------------------

    def cancel(self) -> None:
        """
        Request cancellation of the current scan.
        """

        if self.state in {
            ScanState.COMPLETED,
            ScanState.ERROR,
            ScanState.CANCELLED,
            ScanState.IDLE,
        }:

            return

        self._cancel_requested = True

        self.context.completed_at = datetime.now()

        self._transition(
            ScanState.CANCELLED
        )

    # ----------------------------------------------------------
    # RESET
    # ----------------------------------------------------------

    def reset(self) -> None:
        """
        Reset the workflow so another scan can start.
        """

        if self.state == ScanState.IDLE:

            return

        self.state_manager.reset()

        self.context.state = ScanState.IDLE

        self.context.progress = 0

        self.context.error = None

        self.context.started_at = None

        self.context.completed_at = None

        self._cancel_requested = False

        self._notify_state_change()

    # ----------------------------------------------------------
    # INTERNAL
    # ----------------------------------------------------------

    def _transition(
        self,
        new_state: ScanState,
    ) -> None:

        self.state_manager.transition_to(
            new_state
        )

        self._notify_state_change()

    def _ensure_not_cancelled(self) -> None:

        if self._cancel_requested:

            raise RuntimeError(
                "The scan has been cancelled."
            )