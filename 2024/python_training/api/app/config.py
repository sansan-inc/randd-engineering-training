from functools import cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    is_local: bool = Field(default=False, validation_alias="IS_LOCAL")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    request_timeout: int = Field(default=55, validation_alias="REQUEST_TIMEOUT")
    batch_result_s3_url_base: str = Field(default="", validation_alias="BATCH_RESULT_S3_URL_BASE")


@cache
def get_settings() -> Settings:
    return Settings()
