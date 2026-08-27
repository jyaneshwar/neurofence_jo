"""
Tests for the NeuroFence Day 7 inference engine.
"""

import pytest

from scanner.inference import ModelInference


def test_inference_engine_can_be_created():

    inference = ModelInference()

    assert inference is not None


def test_inference_engine_starts_unloaded():

    inference = ModelInference()

    assert inference.is_loaded() is False


def test_generate_requires_loaded_model():

    inference = ModelInference()

    with pytest.raises(RuntimeError):

        inference.generate(
            "Test prompt"
        )


def test_empty_prompt_is_rejected_after_loading():

    inference = ModelInference()

    inference.loaded = True

    with pytest.raises(ValueError):

        inference.generate("")