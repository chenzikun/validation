#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import json

__author__ = "chenzikun"

import os
import tempfile

import pytest


# -------------------------------------------


@pytest.fixture
def client(app):
    db_fd, _ = tempfile.mkstemp()
    app.config['TESTING'] = True

    client = app.test_client()
    # with app.app_context():
    #     flaskr.init_db()

    yield client
    os.close(db_fd)


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


def test_invalid_request(client):
    data = {
        "apikey": "di2kd92lsdf92.o23o3sf233lkjsf.sdfkjo2i3lkjsldkfj234df",
        # "source": "NGAF",
        "deviceId": "ABCDEFG",
        "deviceVersion": "AF8.0.5 build 0630 R1",
        "sdkVersion": "1.0.0",
        "requestId": "abcdef",
    }
    rv = client.post("/auth", data=json.dumps(data))
    res = json.loads(rv.data)

    print(res)
    assert res["code"] == 1001
    assert res["message"] == "params wrong"
