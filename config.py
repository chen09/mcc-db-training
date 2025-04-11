import logging
from typing import Union

from pydantic import Field
from pydantic_settings import BaseSettings

PROJECT_NAME = "Tools"


class Settings(BaseSettings):
    DATABASE_DEV_URI: str = Field(default="")
    DATABASE_PROD_URI: str = Field(default="")
    FILEHANDLER_LOG_LEVEL: str = Field(default="INFO")


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()


def setup_logging():
    logging.basicConfig(
        format="%(levelname)s: [%(asctime)s] (%(name)s) %(message)s",
        level=getattr(logging, settings.FILEHANDLER_LOG_LEVEL),
    )
    if settings.LOG_OUTPUT_SQL:  # pragma: no cover
        logging.getLogger("sqlalchemy.engine").setLevel(getattr(logging, settings.FILEHANDLER_LOG_LEVEL))
