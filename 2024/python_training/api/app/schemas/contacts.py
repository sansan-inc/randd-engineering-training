from datetime import datetime
from typing import ClassVar

import pandera as pa
from pandera.typing import Series
from pydantic import BaseModel, RootModel


class ContactHistorySchema(pa.SchemaModel):
    owner_user_id: Series[str] = pa.Field(nullable=False)
    owner_company_id: Series[str] = pa.Field(nullable=False)
    user_id: Series[str] = pa.Field(nullable=False)
    company_id: Series[str] = pa.Field(nullable=False)
    created_at: Series[datetime] = pa.Field(nullable=True)

    class Config:
        to_format = "dict"
        to_format_kwargs: ClassVar[dict] = {"orient": "records"}
        coerce = True


class ContactHistoryResponse(BaseModel):
    owner_user_id: str
    owner_company_id: str
    user_id: str
    company_id: str
    created_at: datetime


ContactHistoriesResponse = RootModel[list[ContactHistoryResponse]]
