from functools import cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    is_local: str = Field("false", env="IS_LOCAL")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    batch_result_s3_url_base: str = Field("", env="BATCH_RESULT_S3_URL_BASE")


@cache
def get_setting() -> Settings:
    return Settings()
