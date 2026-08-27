"""
NeuroFence Model Inference Engine.

Day 7:
Provides a controlled interface for loading a
Transformers-compatible language model and generating
responses to security test prompts.
"""

from pathlib import Path
from typing import Optional

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)


class ModelInference:
    """
    Handles loading and running inference on a language model.
    """

    def __init__(self):

        self.model = None
        self.tokenizer = None

        self.model_path: Optional[str] = None

        self.loaded = False

    # ========================================================
    # LOAD MODEL
    # ========================================================

    def load_model(
        self,
        model_path: str,
    ):
        """
        Load a Transformers-compatible model.

        Parameters
        ----------
        model_path:
            Directory containing the model files.
        """

        path = Path(model_path)

        if not path.exists():

            raise FileNotFoundError(
                f"Model directory does not exist: {model_path}"
            )

        if not path.is_dir():

            raise ValueError(
                f"Model path is not a directory: {model_path}"
            )

        try:

            self.tokenizer = AutoTokenizer.from_pretrained(
                str(path),
                local_files_only=True,
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                str(path),
                local_files_only=True,
                torch_dtype=torch.float32,
            )

            self.model.eval()

            self.model_path = str(
                path.resolve()
            )

            self.loaded = True

        except Exception as exc:

            self.model = None
            self.tokenizer = None
            self.model_path = None
            self.loaded = False

            raise RuntimeError(
                f"Unable to load model: {exc}"
            ) from exc

    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 128,
    ) -> str:
        """
        Generate a response from the loaded model.
        """

        if not self.loaded:

            raise RuntimeError(
                "No model is loaded."
            )

        if not prompt.strip():

            raise ValueError(
                "Prompt cannot be empty."
            )

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
        )

        with torch.no_grad():

            output = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
            )

        response = self.tokenizer.decode(
            output[0],
            skip_special_tokens=True,
        )

        return response

    # ========================================================
    # UNLOAD MODEL
    # ========================================================

    def unload_model(self):
        """
        Release the loaded model.
        """

        self.model = None
        self.tokenizer = None

        self.model_path = None

        self.loaded = False

        if torch.cuda.is_available():

            torch.cuda.empty_cache()

    # ========================================================
    # STATUS
    # ========================================================

    def is_loaded(self) -> bool:
        """
        Return whether a model is currently loaded.
        """

        return self.loaded
