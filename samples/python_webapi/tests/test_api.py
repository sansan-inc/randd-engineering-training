import pytest

from randd_sample import api


@pytest.fixture
def client():
    app = api.create_app()
    app.testing = True
    return app.test_client()


def test_health_check(client):
    rv = client.get("/")
    assert rv.data.decode("utf-8") == "I'm fine. Thank you, and you ?"
    assert rv.status_code == 200
