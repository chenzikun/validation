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

    validator_manager = ValidatorManager(app)
    app.validator_manager = validator_manager
    validator = RequestValidator("name", required=True)
    app.validator_manager.register_global_validator(validator)

    client = app.test_client()
    # with app.app_context():
    #     flaskr.init_db()

    yield client

    os.close(db_fd)
    # os.unlink(app.config['DATABASE'])


def test_invalid_request(client):
    rv = client.post("/")
    res = json.loads(rv.data)
    assert rv.status_code == 200
    assert res["code"] == 1001
    assert res["message"] == "params wrong"


def test_index(client):
    data = json.dumps({"name": "chenzikun"})
    rv = client.post("/", data=data)

    assert rv.status_code == 200
    assert rv.data == b'hello'
