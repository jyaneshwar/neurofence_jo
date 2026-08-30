"""
Tests for the NeuroFence Day 9 activation tracker.
"""

import pytest
import torch

from scanner.activation_tracker import (
    ActivationResult,
    ActivationTracker,
)


def test_activation_tracker_can_be_created():

    tracker = ActivationTracker()

    assert tracker is not None


def test_activation_is_analyzed():

    tracker = ActivationTracker()

    activation = torch.tensor(
        [1.0, 2.0, 3.0, 4.0]
    )

    result = tracker.analyze(
        "layer_1",
        activation,
    )

    assert isinstance(
        result,
        ActivationResult,
    )

    assert result.layer_name == "layer_1"

    assert result.shape == [4]

    assert result.mean == pytest.approx(2.5)

    assert result.minimum == pytest.approx(1.0)

    assert result.maximum == pytest.approx(4.0)


def test_normal_activation_has_no_anomaly():

    tracker = ActivationTracker(
        threshold=10.0
    )

    activation = torch.tensor(
        [0.5, 1.0, 1.5, 2.0]
    )

    result = tracker.analyze(
        "layer_1",
        activation,
    )

    assert result.anomaly_detected is False

    assert result.anomaly_reason is None


def test_large_activation_is_detected():

    tracker = ActivationTracker(
        threshold=10.0
    )

    activation = torch.tensor(
        [1.0, 2.0, 15.0, 3.0]
    )

    result = tracker.analyze(
        "layer_2",
        activation,
    )

    assert result.anomaly_detected is True

    assert result.anomaly_reason is not None


def test_empty_activation_is_rejected():

    tracker = ActivationTracker()

    activation = torch.tensor([])

    with pytest.raises(ValueError):

        tracker.analyze(
            "layer_1",
            activation,
        )


def test_invalid_layer_name_is_rejected():

    tracker = ActivationTracker()

    activation = torch.tensor(
        [1.0, 2.0]
    )

    with pytest.raises(ValueError):

        tracker.analyze(
            "",
            activation,
        )


def test_results_are_stored():

    tracker = ActivationTracker()

    activation = torch.tensor(
        [1.0, 2.0, 3.0]
    )

    tracker.analyze(
        "layer_1",
        activation,
    )

    tracker.analyze(
        "layer_2",
        activation,
    )

    results = tracker.get_results()

    assert len(results) == 2


def test_clear_removes_results():

    tracker = ActivationTracker()

    activation = torch.tensor(
        [1.0, 2.0, 3.0]
    )

    tracker.analyze(
        "layer_1",
        activation,
    )

    tracker.clear()

    assert tracker.get_results() == []