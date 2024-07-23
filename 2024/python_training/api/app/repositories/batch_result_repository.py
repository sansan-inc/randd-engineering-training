import json
from abc import ABCMeta, abstractmethod
from pathlib import Path

import s3fs
from s3path import S3Path

from app.config import get_settings
from app.log import get_logger

logger = get_logger(get_settings().log_level)


class IBatchResultRepository(metaclass=ABCMeta):
    @property
    @abstractmethod
    def similar_persons(self) -> dict[str, list[dict]]:
        raise NotImplementedError


class BatchResultRepository(IBatchResultRepository):
    """S3からバッチ結果を取得"""

    def __init__(self, batch_result_s3_url_base: str) -> None:
        logger.info("Start initializing", class_name=self.__class__.__name__)
        self.s3_path = S3Path.from_uri(batch_result_s3_url_base)
        self._similar_persons = self.get_batch_result()
        logger.info("Finish initializing", class_name=self.__class__.__name__)

    def get_batch_result(self) -> dict[str, list[dict]]:
        prediction_result_path = self.s3_path / "predicted_similar_persons.json"
        fs = s3fs.S3FileSystem(anon=False)
        with fs.open(prediction_result_path.as_uri(), "r") as f:
            return json.load(f)

    @property
    def similar_persons(self) -> dict[str, list[dict]]:
        return self._similar_persons


class BatchResultLocalFileRepository(IBatchResultRepository):
    """ローカルからバッチ結果を取得"""

    def __init__(self) -> None:
        logger.info("Start initializing", class_name=self.__class__.__name__)
        self._similar_persons = self.get_batch_result()
        logger.info("Finish initializing", class_name=self.__class__.__name__)

    def get_batch_result(self) -> dict[str, list[dict]]:
        local_json_path = Path(__file__).parents[2] / "data" / "predicted_similar_persons_dummy.json"
        return json.loads(local_json_path.read_text())

    @property
    def similar_persons(self) -> dict[str, list[dict]]:
        return self._similar_persons
