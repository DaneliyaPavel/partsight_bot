"""
Простейший кеш «последний акт» для каждого пользователя.
Хранится в data/last_act.json  вида
{
    "185420810": "BQACAgQAAxkBAAIBT2Y..."
}
Для прод-версии лучше вынести в Redis / SQLite,
но локального файла достаточно.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from loguru import logger

_DATA_DIR = Path("data")
_DATA_DIR.mkdir(exist_ok=True)

_FILE = _DATA_DIR / "last_act.json"


def _load() -> Dict[str, str]:
    if _FILE.exists():
        try:
            return json.loads(_FILE.read_text())
        except Exception as exc:  # повреждён файл
            logger.warning("last_act cache corrupt: {}", exc)
    return {}


def _save(data: Dict[str, str]) -> None:
    _FILE.write_text(json.dumps(data))


# ─────────────────── публичное API ────────────────────
def exists(user_id: int) -> bool:  # ← эта функция нужна inline.py
    return str(user_id) in _load()


def get(user_id: int) -> str | None:
    """Вернёт cached file_id или None."""
    return _load().get(str(user_id))


def set_(user_id: int, file_id: str) -> None:
    """Сохраняем file_id последнего акта."""
    data = _load()
    data[str(user_id)] = file_id
    _save(data)
    logger.info("Cache last_act set for {}: {}", user_id, file_id)
