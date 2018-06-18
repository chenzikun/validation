import pytest
from mock import PropertyMock
import mock

from validations.request_validator import RequestValidator, JSONRPCKeyNotExist, JSONRPCValidationError, \
    JSONRPCInvalidRequest
from validations.validators import OneOf


def test_request_validator():
    with mock.patch('validations.request_validator.RequestValidator.data', new_callable=PropertyMock) as mock_data:
        mock_data.return_value = {"name": "soapa"}
        req_val = RequestValidator(key="name", required=True)
        assert req_val.data == {"name": "soapa"}

        RequestValidator(key="name", required=True)()

        with pytest.raises(JSONRPCInvalidRequest):
            RequestValidator(key="soapa", required=True)()

        validator = OneOf(["soapa", "sdf"])
        RequestValidator(key="name", required=True, validator=validator)()

        with pytest.raises(JSONRPCInvalidRequest):
            validator = OneOf(["sa", "pa"])
            RequestValidator(key="name", required=True, validator=validator)()
