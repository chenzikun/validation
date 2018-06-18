import pytest

from validations.validators import ValidationError, ValidationRegexpError, ValidationOneOfError


def test_validation():
    try:
        raise ValidationRegexpError
    except ValidationError as e:
        assert str(e) == "string is not match pattern"

    try:
        raise ValidationRegexpError("is not match pattern")
    except ValidationError as e:
        assert str(e) == "is not match pattern"

    try:
        raise ValidationOneOfError
    except ValidationError as e:
        assert str(e) == "your put is not expected"

    try:
        raise ValidationOneOfError("custom error message")
    except ValidationError as e:
        assert str(e) == "custom error message"

    with pytest.raises(ValidationError):
        raise ValidationOneOfError

    with pytest.raises(ValidationError):
        raise ValidationRegexpError
