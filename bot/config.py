from __future__ import annotations

import re
from pathlib import Path
from typing import Set

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent  # bot/
DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = BASE_DIR / "templates"


class Settings(BaseSettings):
    # ───── Telegram ─────
    BOT_TOKEN: str
    PROXY_URL: str | None = None
    ADMINS: Set[int] = set()

    # ───── Файлы ─────
    TEMPLATE_PATH: Path = TEMPLATE_DIR / "Акт_шаблон_первый.docx"
    TEMPLATE_TABLE_PATH: Path = TEMPLATE_DIR / "Акт_шаблон_таблица.docx"
    CATALOG_PATH: Path = DATA_DIR / "КАТАЛОГ.xlsb"

    # ───── Валидатор ADMINS ─────
    @field_validator("ADMINS", mode="before")
    def _parse_admins(cls, v):
        if v in (None, "", set()):
            return set()
        if isinstance(v, int):
            return {v}
        if isinstance(v, (set, list, tuple)):
            return {int(x) for x in v}
        if isinstance(v, str):
            parts = re.split(r"[,\s]+", v.strip())
            return {int(p) for p in parts if p}
        raise ValueError("Не могу разобрать ADMINS")

    # ───── pydantic-settings ─────
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid",
    )


settings = Settings()

# гарантируем, что bot/data/ существует
settings.CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
