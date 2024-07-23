from abc import ABCMeta, abstractmethod
from pathlib import Path

import pandas as pd
from google.cloud import bigquery
from pandera.typing import DataFrame

from app.config import get_settings
from app.log import get_logger
from app.schemas.cards import BusinessCardSchema
from app.schemas.contacts import ContactHistorySchema

logger = get_logger(get_settings().log_level)


class IBusinessCardRepository(metaclass=ABCMeta):
    @property
    @abstractmethod
    def business_cards_df(self) -> DataFrame[BusinessCardSchema]:
        raise NotImplementedError

    @property
    @abstractmethod
    def contacts_df(self) -> DataFrame[ContactHistorySchema]:
        raise NotImplementedError


class BusinessCardRepository(IBusinessCardRepository):
    """Colossusからダミー名刺、交換履歴を取得"""

    def __init__(self) -> None:
        logger.info("Start initializing", class_name=self.__class__.__name__)
        self.client = bigquery.Client()
        self._business_cards_df = self.get_business_cards()
        self._contacts_df = self.get_contacts()
        logger.info("Finish initializing", class_name=self.__class__.__name__)

    def get_business_cards(self) -> DataFrame[BusinessCardSchema]:
        sql = """
            SELECT
                user_id,
                company_id,
                full_name,
                position,
                company_name,
                address,
                phone_number
            FROM
                `gcp_project.dataset.dummy_business_cards`
        """
        return self.client.query(sql).to_dataframe()

    def get_contacts(self) -> DataFrame[ContactHistorySchema]:
        sql = """
            SELECT
                owner_user_id,
                owner_company_id,
                user_id,
                company_id,
                created_at
            FROM
                `gcp_project.dataset.dummy_business_cards_exchange_history`
        """
        return self.client.query(sql).to_dataframe()

    @property
    def business_cards_df(self) -> DataFrame[BusinessCardSchema]:
        return self._business_cards_df

    @property
    def contacts_df(self) -> DataFrame[ContactHistorySchema]:
        return self._contacts_df


class BusinessCardLocalFileRepository(IBusinessCardRepository):
    """ローカルからダミー名刺の情報取得"""

    def __init__(self) -> None:
        logger.info("Start initializing", class_name=self.__class__.__name__)
        self.data_dir = Path(__file__).parents[2] / "data"
        self._business_cards_df = self.get_business_cards()
        self._contacts_df = self.get_contacts()
        logger.info("Finish initializing", class_name=self.__class__.__name__)

    def get_business_cards(self) -> DataFrame[BusinessCardSchema]:
        return pd.read_csv(self.data_dir / "dummy_business_cards.csv", dtype=str)

    def get_contacts(self) -> DataFrame[ContactHistorySchema]:
        contacts_df = pd.read_csv(self.data_dir / "dummy_business_cards_exchange_history.csv", dtype=str)
        contacts_df["created_at"] = pd.to_datetime(contacts_df["created_at"])
        return contacts_df

    @property
    def business_cards_df(self) -> DataFrame[BusinessCardSchema]:
        return self._business_cards_df

    @property
    def contacts_df(self) -> DataFrame[ContactHistorySchema]:
        return self._contacts_df
