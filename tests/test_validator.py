import pytest

from validations.validators import Regexp, ValidationError, OneOf, IsaAlphaNumber


def test_regexp():
    regex = Regexp(r"[A-Za-z0-9\.]{15,30}")
    data = "1234ds34655.46addsf256"
    assert regex(data)

    with pytest.raises(ValidationError):
        data = "12435y8%(dsfjsdfg"
        assert regex(data)

    with pytest.raises(ValidationError):
        data = "1234d s34655.46a ddsf256"
        assert regex(data)

    deviceId_val = Regexp(r"[A-Za-z0-9\s\.]{20}")
    data = "AF8.0.5 build 0630 R1"
    assert deviceId_val(data)


def test_oneof():
    oneof = OneOf([1, 2, 3])
    assert oneof(1)
    with pytest.raises(ValidationError):
        oneof(4)


def test_isalphanumber():
    isalnum = IsaAlphaNumber(". ")
    assert isalnum("1234. akjdfg")

    with pytest.raises(ValidationError):
        data = "$jshdf"
        assert isalnum(data)
