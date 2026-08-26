"""
NeuroFence - Scan Result

Stores the final result produced by a security scan.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ScanResult:
    """
    Represents the result of a completed security scan.
    """

    model_path: str

    scan_id: str = ""

    prompts_tested: int = 0

    suspicious_outputs: int = 0

    threat_score: float = 0.0

    threat_level: str = "LOW"

    findings: List[str] = field(
        default_factory=list
    )

    errors: List[str] = field(
        default_factory=list
    )

    scan_duration_seconds: float = 0.0

    completed: bool = False