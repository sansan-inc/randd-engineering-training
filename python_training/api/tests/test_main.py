from collections.abc import Generator
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.main import app, container
from app.services.batch_result_service import BatchResultService


@pytest.fixture(scope="function")
def dummy_batch_result_service(request: pytest.FixtureRequest) -> Mock:
    get_data_return_value = getattr(request, "param", {})
    batch_result_service_mock = Mock(spec=BatchResultService)
    batch_result_service_mock.get_data.return_value = get_data_return_value
    return batch_result_service_mock


@pytest.fixture(scope="session")
def test_client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


def test_get_root(test_client: TestClient) -> None:
    response = test_client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("dummy_batch_result_service", "expected_list_persons"),
    [
        ({"sato": []}, {"names": ["sato"]}),
        ({"suzuki": [], "sato": []}, {"names": ["suzuki", "sato"]}),
    ],
    indirect=["dummy_batch_result_service"],
)
def test_get_list_persons(
    test_client: TestClient, dummy_batch_result_service: Mock, expected_list_persons: list[dict[str, int | str]]
) -> None:
    with container.batch_result_service.override(dummy_batch_result_service):
        response = test_client.get("/persons/")
        assert response.status_code == 200
        assert response.json() == expected_list_persons


def test_get_list_persons_422(
    test_client: TestClient,
    dummy_batch_result_service: Mock,
) -> None:
    """query parameterがintではなくstring型で入力されている異常系のテスト"""
    with container.batch_result_service.override(dummy_batch_result_service):
        response = test_client.get("/persons/?limit=a")
        assert response.status_code == 422
        assert response.json() == {
            "detail": [{"loc": ["query", "limit"], "msg": "value is not a valid integer", "type": "type_error.integer"}]
        }


@pytest.mark.parametrize(
    ("path_parameter", "expected_similar_person"),
    [
        ("/persons/sato/", {"names": ["suzuki", "sato"]}),
        ("/persons/suzuki/", {"names": []}),
        ("/persons/tanaka/", {"names": []}),
    ],
    ids=[None, "suzukiは存在しているが, 類似人物がいないため, 空リスト", "tanakaは存在しないため, 空リスト"],
)
@pytest.mark.parametrize(
    ("dummy_batch_result_service",),
    [
        ({"suzuki": [], "sato": ["suzuki", "sato"]},),
    ],
    indirect=["dummy_batch_result_service"],
)
def test_search_similar_person(
    test_client: TestClient,
    path_parameter: str,
    dummy_batch_result_service: Mock,
    expected_similar_person: dict[str, int | str],
) -> None:
    with container.batch_result_service.override(dummy_batch_result_service):
        response = test_client.get(path_parameter)
        assert response.status_code == 200
        assert response.json() == expected_similar_person
