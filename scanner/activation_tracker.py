"""
NeuroFence Day 9 - Activation Tracker.

Collects and analyzes activation statistics from model layers.
"""

from dataclasses import dataclass, field
from typing import List, Optional

import torch


@dataclass
class ActivationResult:
    """Stores statistics for a captured activation."""

    layer_name: str

    shape: List[int]

    mean: float
    std: float

    minimum: float
    maximum: float

    anomaly_detected: bool = False

    anomaly_reason: Optional[str] = None


class ActivationTracker:
    """
    Tracks activation tensors produced by a model.

    Day 9 focuses on the foundation:
    - capturing activations
    - calculating statistics
    - detecting simple statistical anomalies
    """

    def __init__(
        self,
        threshold: float = 10.0,
    ) -> None:

        if threshold <= 0:

            raise ValueError(
                "Threshold must be greater than zero."
            )

        self.threshold = threshold

        self.results: List[ActivationResult] = []

    def analyze(
        self,
        layer_name: str,
        activation: torch.Tensor,
    ) -> ActivationResult:
        """
        Analyze one activation tensor.

        Parameters
        ----------
        layer_name:
            Name of the model layer.

        activation:
            Activation tensor produced by that layer.
        """

        if not layer_name.strip():

            raise ValueError(
                "Layer name cannot be empty."
            )

        if not isinstance(activation, torch.Tensor):

            raise TypeError(
                "Activation must be a torch.Tensor."
            )

        if activation.numel() == 0:

            raise ValueError(
                "Activation tensor cannot be empty."
            )

        tensor = activation.detach().float().cpu()

        mean = tensor.mean().item()

        std = tensor.std(unbiased=False).item()

        minimum = tensor.min().item()

        maximum = tensor.max().item()

        anomaly_detected = False

        anomaly_reason = None

        if abs(maximum) >= self.threshold:

            anomaly_detected = True

            anomaly_reason = (
                f"Maximum activation {maximum:.4f} "
                f"exceeded threshold {self.threshold:.4f}."
            )

        elif abs(minimum) >= self.threshold:

            anomaly_detected = True

            anomaly_reason = (
                f"Minimum activation {minimum:.4f} "
                f"exceeded threshold {self.threshold:.4f}."
            )

        result = ActivationResult(
            layer_name=layer_name,
            shape=list(tensor.shape),
            mean=mean,
            std=std,
            minimum=minimum,
            maximum=maximum,
            anomaly_detected=anomaly_detected,
            anomaly_reason=anomaly_reason,
        )

        self.results.append(result)

        return result

    def clear(self) -> None:
        """Clear all previously recorded activation results."""

        self.results.clear()

    def get_results(self) -> List[ActivationResult]:
        """Return all recorded activation results."""

        return list(self.results)