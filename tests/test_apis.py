import os
import tempfile

import pytest
from flask import json

from validations.managers import ValidatorManager
from validations.request_validator import RequestValidator


@pytest.fixture
def client(app):
    db_fd, _ = tempfile.mkstemp()
    app.config['TESTING'] = True

    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(_)


def test_request(client):
    data = {
        "apikey": "di2kd92lsdf92.o23o3sf233lkjsf.sdfkjo2i3lkjsldkfj234df",
        "source": "NGAF",
        "deviceId": "ABCDEFG",
        "deviceVersion": "AF8.0.5 build 0630 R1",
        "sdkVersion": "1.0.0",
        "requestId": "abcdef",
    }
    rv = client.post("/auth", data=json.dumps(data))
    res = json.loads(rv.data)
    assert res["code"] == 0
    assert res["message"] == "auth"
