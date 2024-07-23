import pandera as pa
from pandera.typing import Series


class PersonSchema(pa.SchemaModel):
    user_id: Series[str] = pa.Field(nullable=False)
    company_id: Series[str] = pa.Field(nullable=False)
    full_name: Series[str] = pa.Field(nullable=False)
    company_name: Series[str] = pa.Field(nullable=False)
    address: Series[str] = pa.Field(nullable=False)
    phone_number: Series[str] = pa.Field(nullable=False)


class SimilarPersonSchema(PersonSchema):
    similarity: Series[float] | None = pa.Field(nullable=True)
