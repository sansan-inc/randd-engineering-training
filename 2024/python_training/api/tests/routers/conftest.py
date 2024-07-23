import os
from collections.abc import Generator
from unittest import mock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def test_client() -> Generator[TestClient, None, None]:
    with mock.patch.dict(os.environ, {"IS_LOCAL": "True"}):
        from app.main import app

        with TestClient(app) as client:
            yield client
