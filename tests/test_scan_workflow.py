"""
NeuroFence - Scan Workflow Tests

Tests the security scan lifecycle, state transitions,
progress tracking, cancellation, error handling,
reset behavior, and state listeners.
"""

import pytest

from scanner.state import ScanState
from scanner.workflow import ScanWorkflow


# ================================================================
# TEST HELPER
# ================================================================

def create_workflow():
    """
    Create a fresh ScanWorkflow instance for testing.
    """

    return ScanWorkflow(
        scan_id="TEST-001",
        model_path="sample_models/demo_model",
    )


# ================================================================
# INITIAL STATE
# ================================================================

def test_initial_state():
    """
    A newly created workflow should begin in IDLE state.
    """

    workflow = create_workflow()

    assert workflow.state == ScanState.IDLE

    assert workflow.progress == 0


# ================================================================
# NORMAL SCAN LIFECYCLE
# ================================================================

def test_normal_scan_lifecycle():
    """
    Verify the complete normal scan lifecycle:

    IDLE
        ↓
    LOADING
        ↓
    SCANNING
        ↓
    ANALYZING
        ↓
    COMPLETED
    """

    workflow = create_workflow()

    # Start scan
    workflow.start()

    assert workflow.state == ScanState.LOADING

    # Begin scanning
    workflow.begin_scanning()

    assert workflow.state == ScanState.SCANNING

    # Update progress
    workflow.update_progress(50)

    assert workflow.progress == 50

    # Begin analysis
    workflow.begin_analysis()

    assert workflow.state == ScanState.ANALYZING

    # Complete scan
    workflow.complete()

    assert workflow.state == ScanState.COMPLETED

    assert workflow.progress == 100


# ================================================================
# INVALID STATE TRANSITION
# ================================================================

def test_invalid_transition():
    """
    Attempting to move directly from IDLE to SCANNING
    should raise ValueError.
    """

    workflow = create_workflow()

    with pytest.raises(ValueError):

        workflow.begin_scanning()


# ================================================================
# PROGRESS VALIDATION
# ================================================================

def test_progress_validation():
    """
    Progress must always remain between 0 and 100.
    """

    workflow = create_workflow()

    workflow.start()

    # Valid progress
    workflow.update_progress(50)

    assert workflow.progress == 50

    # Progress above 100
    with pytest.raises(ValueError):

        workflow.update_progress(101)

    # Progress below 0
    with pytest.raises(ValueError):

        workflow.update_progress(-1)


# ================================================================
# ERROR HANDLING
# ================================================================

def test_scan_error():
    """
    A scan failure should move the workflow into ERROR state
    and preserve the error message.
    """

    workflow = create_workflow()

    workflow.start()

    workflow.begin_scanning()

    workflow.fail(
        "Test scanner failure"
    )

    assert workflow.state == ScanState.ERROR

    assert (
        workflow.context.error
        == "Test scanner failure"
    )


# ================================================================
# CANCELLATION
# ================================================================

def test_scan_cancellation():
    """
    A running scan should be able to enter CANCELLED state.
    """

    workflow = create_workflow()

    workflow.start()

    workflow.cancel()

    assert workflow.state == ScanState.CANCELLED


# ================================================================
# RESET
# ================================================================

def test_reset():
    """
    A completed scan should be resettable to IDLE.
    """

    workflow = create_workflow()

    workflow.start()

    workflow.begin_scanning()

    workflow.begin_analysis()

    workflow.complete()

    assert workflow.state == ScanState.COMPLETED

    workflow.reset()

    assert workflow.state == ScanState.IDLE

    assert workflow.progress == 0

    assert workflow.context.error is None

    assert workflow.context.started_at is None

    assert workflow.context.completed_at is None


# ================================================================
# STATE LISTENER
# ================================================================

def test_state_listener():
    """
    Verify that registered listeners receive every
    state transition.
    """

    workflow = create_workflow()

    states = []

    workflow.add_listener(
        states.append
    )

    workflow.start()

    workflow.begin_scanning()

    workflow.begin_analysis()

    workflow.complete()

    assert states == [
        ScanState.LOADING,
        ScanState.SCANNING,
        ScanState.ANALYZING,
        ScanState.COMPLETED,
    ]


# ================================================================
# TEST COMPLETION
# ================================================================

if __name__ == "__main__":
    pytest.main(
        [
            "-v",
            __file__,
        ]
    )