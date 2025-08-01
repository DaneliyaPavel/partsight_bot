from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    BOT_TOKEN: str
    PROXY_URL: str | None = None
    TEMPLATE_PATH: Path = Path("templates/Акт_шаблон_первый.docx")
    TEMPLATE_TABLE_PATH: Path = Path("templates/Акт_шаблон_таблица.docx")
    CATALOG_PATH: Path = Path("bot/data/КАТАЛОГ.xlsb")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
