from pydantic import BaseModel, Field


class Persons(BaseModel):
    names: list[str] = Field([], example=["sato"])
