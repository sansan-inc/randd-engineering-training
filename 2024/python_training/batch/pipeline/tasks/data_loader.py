from logging import getLogger

from google.cloud import bigquery

from pipeline.utils.template import GokartTask

logger = getLogger(__name__)


class LoadCardDataTask(GokartTask):
    """Colossusからダミーデータを取得"""

    def run(self) -> None:
        sql = """
            SELECT
                owner_user_id,
                company_id,
            FROM
                `gcp_project.dataset.dummy_business_cards_exchange_history`
        """
        client = bigquery.Client()
        data_frame = client.query(sql).to_dataframe()
        self.dump(data_frame)
