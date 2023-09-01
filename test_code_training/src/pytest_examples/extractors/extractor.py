from pytest_examples.clients.protocol import IClient
from pytest_examples.models.random_model import RandomModel
from pytest_examples.preprocessors.protocol import IPreprocessor


class Extractor:
    def __init__(self, preprocessor: IPreprocessor, model: RandomModel, storage_client: IClient) -> None:
        self.preprocessor = preprocessor
        self.model = model
        self.storage_client = storage_client

    def extract(self, document_id: str) -> str:
        input_text = self.storage_client.get_text(document_id)
        preprocessed_text = self.preprocessor(input_text)
        model_output = self.model.predict(preprocessed_text)
        start_position = model_output.start_position
        end_position = model_output.end_position
        return preprocessed_text[start_position:end_position]
