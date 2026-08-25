from model_loader.validator import ModelValidator


def test_validator_can_be_created():

    validator = ModelValidator()

    assert validator is not None


def test_project_root_is_not_a_model():

    validator = ModelValidator()

    result = validator.validate(".")

    assert result.valid is False


def test_missing_model_directory():

    validator = ModelValidator()

    result = validator.validate(
        "this_directory_does_not_exist"
    )

    assert result.valid is False