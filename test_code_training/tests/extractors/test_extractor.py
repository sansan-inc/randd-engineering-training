from unittest.mock import Mock

import pytest

from pytest_examples.clients.protocol import IClient
from pytest_examples.extractors.extractor import Extractor
from pytest_examples.models.random_model import RandomModel
from pytest_examples.preprocessors.protocol import IPreprocessor
from pytest_examples.schemas.model_output import ModelOutput


class TestExtractor:
    @pytest.fixture(scope="class")
    def dummy_preprocessor(self, request: pytest.FixtureRequest) -> Mock:
        preprocessor_mock = Mock(spec=IPreprocessor)
        preprocessor_mock.return_value = request.param
        return preprocessor_mock

    @pytest.fixture(scope="class")
    def dummy_model(self, request: pytest.FixtureRequest) -> Mock:
        model_mock = Mock(spec=RandomModel)
        model_mock.predict.return_value = request.param
        return model_mock

    @pytest.fixture(scope="class")
    def dummy_storage_client(self) -> Mock:
        storage_client_mock = Mock(spec=IClient)
        storage_client_mock.get_text.return_value = ""  # ここの値は今回テストしたい範囲外のためダミー文字列
        return storage_client_mock

    @pytest.fixture(scope="function")
    def extractor(
        self,
        dummy_preprocessor: Mock,
        dummy_model: Mock,
        dummy_storage_client: Mock,
    ) -> Extractor:
        return Extractor(
            preprocessor=dummy_preprocessor,
            model=dummy_model,
            storage_client=dummy_storage_client,
        )

    @pytest.mark.parametrize(
        ("dummy_preprocessor", "dummy_model", "extracted_text"),
        [
            ("Sansan株式会社", ModelOutput(text_length=10, start_position=0, end_position=6), "Sansan"),
        ],
        indirect=["dummy_preprocessor", "dummy_model"],
    )
    def test_extract(self, extractor: Extractor, extracted_text: str) -> None:
        assert extractor.extract(document_id="33") == extracted_text
