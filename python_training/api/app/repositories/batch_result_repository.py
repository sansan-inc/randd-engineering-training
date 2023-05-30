import json
from abc import ABCMeta, abstractmethod
from pathlib import Path

import s3fs
from s3path import S3Path


class IBatchResultRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self) -> dict[str, list[str]]:
        raise NotImplementedError()


class BatchResultRepository(IBatchResultRepository):
    """S3からバッチ結果を取得"""

    def __init__(self, batch_result_s3_url_base: str) -> None:
        s3_path = S3Path.from_uri(batch_result_s3_url_base) / "predicted_similar_persons.json"
        fs = s3fs.S3FileSystem(anon=False)
        with fs.open(s3_path.as_uri(), "r") as f:
            self._predictions: dict[str, list[str]] = json.load(f)

    def get_data(self) -> dict[str, list[str]]:
        return self._predictions


class BatchResultLocalFileRepository(IBatchResultRepository):
    """ローカルからバッチ結果を取得"""

    def __init__(self) -> None:
        local_json_path = Path(__file__).parents[1] / "data" / "predicted_similar_persons_dummy.json"
        with local_json_path.open("r") as f:
            self._predictions: dict[str, list[str]] = json.load(f)

    def get_data(self) -> dict[str, list[str]]:
        return self._predictions
