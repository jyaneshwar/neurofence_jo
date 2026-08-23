"""
NeuroFence model directory validator.

Day 4:
Validates the basic structure of a local LLM model directory.
"""

from pathlib import Path

from model_loader.result import ModelValidationResult


class ModelValidator:
    """Validate a local model directory."""

    CONFIG_FILES = {
        "config.json",
    }

    WEIGHT_FILES = {
        "pytorch_model.bin",
        "model.safetensors",
        "pytorch_model.bin.index.json",
        "model.safetensors.index.json",
    }

    TOKENIZER_FILES = {
        "tokenizer.json",
        "tokenizer_config.json",
        "tokenizer.model",
    }

    def validate(
        self,
        model_path: str,
    ) -> ModelValidationResult:
        """
        Validate a model directory.

        Parameters
        ----------
        model_path:
            Path to the local model directory.

        Returns
        -------
        ModelValidationResult
            Validation result.
        """

        result = ModelValidationResult(
            model_path=model_path
        )

        if not model_path:
            result.errors.append(
                "No model directory was selected."
            )

            return result

        path = Path(model_path)

        # ---------------------------------------------------------
        # Directory validation
        # ---------------------------------------------------------

        if not path.exists():
            result.errors.append(
                "Selected model directory does not exist."
            )

            return result

        if not path.is_dir():
            result.errors.append(
                "Selected path is not a directory."
            )

            return result

        # ---------------------------------------------------------
        # Collect files
        # ---------------------------------------------------------

        try:
            files = [
                item.name
                for item in path.iterdir()
                if item.is_file()
            ]

        except PermissionError:
            result.errors.append(
                "Permission denied while reading model directory."
            )

            return result

        result.model_files = sorted(
            files
        )

        # ---------------------------------------------------------
        # Config validation
        # ---------------------------------------------------------

        result.config_found = any(
            filename in result.model_files
            for filename in self.CONFIG_FILES
        )

        if not result.config_found:
            result.errors.append(
                "config.json was not found."
            )

        # ---------------------------------------------------------
        # Weight validation
        # ---------------------------------------------------------

        result.weights_found = any(
            filename in result.model_files
            for filename in self.WEIGHT_FILES
        )

        # Check for sharded weight files.
        if not result.weights_found:

            for filename in result.model_files:

                if (
                    filename.startswith(
                        "model-"
                    )
                    and (
                        filename.endswith(
                            ".safetensors"
                        )
                        or filename.endswith(
                            ".bin"
                        )
                    )
                ):
                    result.weights_found = True
                    break

        if not result.weights_found:
            result.errors.append(
                "No supported model weight files were found."
            )

        # ---------------------------------------------------------
        # Tokenizer validation
        # ---------------------------------------------------------

        result.tokenizer_found = any(
            filename in result.model_files
            for filename in self.TOKENIZER_FILES
        )

        if not result.tokenizer_found:
            result.warnings.append(
                "Tokenizer files were not found."
            )

        # ---------------------------------------------------------
        # Final validation
        # ---------------------------------------------------------

        result.valid = (
            result.config_found
            and result.weights_found
            and not result.errors
        )

        return result