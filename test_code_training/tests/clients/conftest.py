from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def root_path() -> Path:
    return Path(__file__).with_name("dummy_documents")
