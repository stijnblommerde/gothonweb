from nose.tools import *
from src.bin import app
from .tools import assert_response


def test_index():

    # status code 303 refers to redirect
    resp = app.request("/")
    assert_response(resp, status="303")

    resp = app.request("/game")
    assert_response(resp, status="200")

    resp = app.request("/game", method="POST")
    assert_response(resp, status="303")
