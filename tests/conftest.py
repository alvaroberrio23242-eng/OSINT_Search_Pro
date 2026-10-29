import os

os.environ.setdefault("OSP_DEV", "1")

import pytest

from app import app as flask_app
from extensions import limiter


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    limiter.reset()
    return flask_app.test_client()
