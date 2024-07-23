import json

import gokart
import luigi
import s3fs
from s3path import S3Path

from pipeline.tasks.data_handler import PredictSimilarNodeTask
from pipeline.utils.template import GokartTask


class UploadPredictedDataTask(GokartTask):
    """
    類似人物の予測結果をS3にアップロードするタスク
    """

    predict_similar_node_task = gokart.TaskInstanceParameter()
    output_result_data_s3_url_base = luigi.Parameter()

    def requires(self) -> PredictSimilarNodeTask:
        return self.predict_similar_node_task

    def run(self) -> None:
        results_json = self.load()
        # コンテナの実行権限に関わらず書き込めるようにアップロード
        upload_s3_path: S3Path = (
            S3Path.from_uri(self.output_result_data_s3_url_base)
            / "predicted_similar_persons.json"
        )
        fs = s3fs.S3FileSystem(anon=False)
        with fs.open(upload_s3_path.as_uri(), "w") as f:
            f.write(json.dumps(results_json))

        self.dump(f"Upload predicted results to {upload_s3_path.as_uri()}.")
