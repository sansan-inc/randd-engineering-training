from typing import ClassVar

import pandera as pa
from pandera.typing import Series
from pydantic import BaseModel, RootModel


class BusinessCardSchema(pa.SchemaModel):
    user_id: Series[str] = pa.Field(nullable=False)
    company_id: Series[str] = pa.Field(nullable=False)
    full_name: Series[str] = pa.Field(nullable=False)
    position: Series[str] = pa.Field(nullable=False)
    company_name: Series[str] = pa.Field(nullable=False)
    address: Series[str] = pa.Field(nullable=False)
    phone_number: Series[str] = pa.Field(nullable=False)
    similarity: Series[float] | None = pa.Field(nullable=True)

    class Config:
        to_format = "dict"
        to_format_kwargs: ClassVar[dict] = {"orient": "records"}
        coerce = True


class BusinessCardResponse(BaseModel):
    user_id: str
    company_id: str
    full_name: str
    position: str
    company_name: str
    address: str
    phone_number: str


class SimilarBusinessCardResponse(BusinessCardResponse):
    similarity: float | None = None


BusinessCardsResponse = RootModel[list[BusinessCardResponse]]
SimilarBusinessCardsResponse = RootModel[list[SimilarBusinessCardResponse]]
