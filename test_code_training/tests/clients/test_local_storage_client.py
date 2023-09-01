from pathlib import Path

import pytest

from pytest_examples.clients.local_storage_client import LocalStorageClient


class TestLocalStorageClient:
    @pytest.fixture(scope="class")
    def local_storage_client(
        self,
        root_path: Path,  # conftest.pyにfixtureが実装されているため, それを参照する
    ) -> LocalStorageClient:
        return LocalStorageClient(root_path)

    @pytest.mark.parametrize(
        ("document_id", "expected_text"),
        [
            ("1", "BBB1 CCC1 OOO1"),
            ("8", "fugahoge"),
            ("33", "Dummy株式会社"),
        ],
    )
    def test_get_text(self, local_storage_client: LocalStorageClient, document_id: str, expected_text: str) -> None:
        assert local_storage_client.get_text(document_id) == expected_text
