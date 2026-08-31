"""
Tests for the NeuroFence Day 10 activation hook manager.
"""

import torch
from torch import nn

from scanner.activation_hooks import (
    ActivationHookManager,
)
from scanner.activation_tracker import (
    ActivationTracker,
)


class SmallTestModel(nn.Module):
    """Small neural network used only for testing hooks."""

    def __init__(self):
        super().__init__()

        self.layer1 = nn.Linear(4, 8)

        self.activation = nn.ReLU()

        self.layer2 = nn.Linear(8, 2)

    def forward(self, x):

        x = self.layer1(x)

        x = self.activation(x)

        x = self.layer2(x)

        return x


def test_hook_manager_can_be_created():

    manager = ActivationHookManager()

    assert manager is not None


def test_hooks_are_attached():

    model = SmallTestModel()

    manager = ActivationHookManager()

    count = manager.attach(model)

    assert count > 0

    manager.remove()


def test_hooks_capture_activations():

    model = SmallTestModel()

    tracker = ActivationTracker(
        threshold=100.0
    )

    manager = ActivationHookManager(
        tracker=tracker
    )

    manager.attach(model)

    input_tensor = torch.randn(
        1,
        4,
    )

    model(input_tensor)

    results = manager.get_results()

    assert len(results) > 0

    assert all(
        result.layer_name
        for result in results
    )

    manager.remove()


def test_results_contain_shapes():

    model = SmallTestModel()

    manager = ActivationHookManager()

    manager.attach(model)

    input_tensor = torch.randn(
        1,
        4,
    )

    model(input_tensor)

    results = manager.get_results()

    assert len(results) > 0

    for result in results:

        assert len(result.shape) > 0

    manager.remove()


def test_clear_results():

    model = SmallTestModel()

    manager = ActivationHookManager()

    manager.attach(model)

    model(
        torch.randn(1, 4)
    )

    assert len(manager.get_results()) > 0

    manager.clear_results()

    assert manager.get_results() == []

    manager.remove()


def test_remove_hooks():

    model = SmallTestModel()

    manager = ActivationHookManager()

    manager.attach(model)

    manager.remove()

    assert len(manager.hooks) == 0