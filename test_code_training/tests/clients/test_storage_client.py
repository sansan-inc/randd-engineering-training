import os
from unittest import mock

import pytest

from pytest_examples.clients.storage_client import StorageClient


class TestStorageClient:
    @mock.patch.dict(os.environ, {"HAS_STORAGE_AUTHORIZATION": "true"})
    def test_initialize(self) -> None:
        StorageClient()

    def test_initialize_permission_error(self) -> None:
        with pytest.raises(PermissionError, match="Not authorized."):
            StorageClient()
