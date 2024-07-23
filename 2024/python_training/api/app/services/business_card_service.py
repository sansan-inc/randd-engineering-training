import datetime

from pandera.typing import DataFrame

from app.repositories import IBusinessCardRepository
from app.schemas.cards import BusinessCardSchema
from app.schemas.contacts import ContactHistorySchema


class BusinessCardService:
    def __init__(self, repository: IBusinessCardRepository) -> None:
        self._repository = repository

    def get_business_card_df(self) -> DataFrame[BusinessCardSchema]:
        return self._repository.business_cards_df

    def get_contacts_df(
        self,
        start_date: datetime.date | None = None,
        end_date: datetime.date | None = None,
    ) -> DataFrame[ContactHistorySchema]:
        contacts_df = self._repository.contacts_df
        if start_date is not None:
            # start_dateとend_dateが同じ日付の場合はその日付のデータのみ取得するようにするため, datetimeをdateに変換
            contacts_df = contacts_df[(contacts_df["created_at"].dt.date >= start_date)]

        if end_date is not None:
            # start_dateとend_dateが同じ日付の場合はその日付のデータのみ取得するようにするため, datetimeをdateに変換
            contacts_df = contacts_df[(contacts_df["created_at"].dt.date <= end_date)]

        return contacts_df
