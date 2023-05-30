from logging import getLogger

import awswrangler as wr
import luigi
from pipeline.utils.template import GokartTask
from s3path import S3Path

logger = getLogger(__name__)


class LoadCardDataTask(GokartTask):
    """Athenaからデータを取得"""

    output_athena_query_s3_url_base = luigi.Parameter()

    def run(self) -> None:
        sql = """
            SELECT
                user_id,
                company_id
            FROM
                sample_business_cards
        """
        output_s3_path: S3Path = S3Path.from_uri(self.output_athena_query_s3_url_base)
        df = wr.athena.read_sql_query(
            sql=sql,
            database="randd_engineering_training_2023",
            s3_output=output_s3_path.as_uri(),
            ctas_approach=False,
        )
        self.dump(df)
