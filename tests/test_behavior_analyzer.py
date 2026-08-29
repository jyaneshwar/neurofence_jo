"""
Tests for the NeuroFence Day 8 behavior analyzer.
"""

import pytest

from scanner.behavior_analyzer import (
    BehaviorAnalyzer,
    BehaviorResult,
)


def test_behavior_analyzer_can_be_created():
    analyzer = BehaviorAnalyzer()

    assert analyzer is not None


def test_refusal_is_detected():
    analyzer = BehaviorAnalyzer()

    result = analyzer.analyze(
        "Tell me something dangerous.",
        "I cannot help with that request.",
    )

    assert isinstance(result, BehaviorResult)
    assert result.refusal_detected is True
    assert result.compliance_score == 0.0


def test_normal_response_has_no_suspicious_indicators():
    analyzer = BehaviorAnalyzer()

    result = analyzer.analyze(
        "What is network security?",
        "Network security protects systems and data from threats.",
    )

    assert result.refusal_detected is False
    assert result.suspicious_indicators == []


def test_suspicious_behavior_is_detected():
    analyzer = BehaviorAnalyzer()

    result = analyzer.analyze(
        "Security test",
        "The response describes how to bypass security and evade detection.",
    )

    assert result.refusal_detected is False
    assert "bypass security" in result.suspicious_indicators
    assert "evade detection" in result.suspicious_indicators
    assert result.behavior_score > 0.0


def test_empty_prompt_is_rejected():
    analyzer = BehaviorAnalyzer()

    with pytest.raises(ValueError):
        analyzer.analyze(
            "",
            "Test response",
        )


def test_empty_response_is_rejected():
    analyzer = BehaviorAnalyzer()

    with pytest.raises(ValueError):
        analyzer.analyze(
            "Test prompt",
            "",
        )