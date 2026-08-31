"""
NeuroFence Day 10 - Activation Hook Manager.

Attaches PyTorch forward hooks to model layers and sends
captured activations to the ActivationTracker.
"""

from typing import Dict, List

import torch
from torch import nn

from scanner.activation_tracker import (
    ActivationResult,
    ActivationTracker,
)


class ActivationHookManager:
    """
    Manages forward hooks for activation monitoring.

    The manager can attach hooks to selected model layers,
    capture their outputs, and pass those outputs to the
    ActivationTracker.
    """

    def __init__(
        self,
        tracker: ActivationTracker | None = None,
    ) -> None:

        self.tracker = tracker or ActivationTracker()

        self.hooks: List[torch.utils.hooks.RemovableHandle] = []

        self.results: List[ActivationResult] = []

    def attach(
        self,
        model: nn.Module,
    ) -> int:
        """
        Attach hooks to supported model layers.

        Returns
        -------
        int
            Number of hooks attached.
        """

        self.remove()

        count = 0

        for name, module in model.named_modules():

            # Skip the root module.
            if not name:
                continue

            # Only attach to leaf modules.
            if list(module.children()):
                continue

            hook = module.register_forward_hook(
                self._create_hook(name)
            )

            self.hooks.append(hook)

            count += 1

        return count

    def _create_hook(self, layer_name: str):

        def hook(
            module: nn.Module,
            inputs,
            output,
        ) -> None:

            tensor = self._extract_tensor(output)

            if tensor is None:
                return

            result = self.tracker.analyze(
                layer_name,
                tensor,
            )

            self.results.append(result)

        return hook

    def _extract_tensor(
        self,
        output,
    ) -> torch.Tensor | None:
        """
        Extract a tensor from a module output.

        Supports:
        - Tensor
        - tuple/list containing a Tensor
        """

        if isinstance(output, torch.Tensor):

            return output

        if isinstance(output, (tuple, list)):

            for item in output:

                if isinstance(item, torch.Tensor):

                    return item

        return None

    def remove(self) -> None:
        """Remove all currently registered hooks."""

        for hook in self.hooks:

            hook.remove()

        self.hooks.clear()

    def clear_results(self) -> None:
        """Clear captured activation results."""

        self.results.clear()

        self.tracker.clear()

    def get_results(self) -> List[ActivationResult]:
        """Return captured activation results."""

        return list(self.results)

    def get_layer_names(self) -> List[str]:
        """Return names of layers that produced results."""

        return [
            result.layer_name
            for result in self.results
        ]