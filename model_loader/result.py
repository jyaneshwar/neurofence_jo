"""
Model validation result objects for NeuroFence.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ModelValidationResult:
    """Stores the result of model directory validation."""

    valid: bool = False

    model_path: str = ""

    config_found: bool = False

    weights_found: bool = False

    tokenizer_found: bool = False

    errors: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    model_files: List[str] = field(
        default_factory=list
    )