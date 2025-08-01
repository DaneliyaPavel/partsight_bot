from __future__ import annotations

import asyncio
import re
from pathlib import Path
from typing import Set

import pandas as pd
from loguru import logger

from bot.config import settings
from bot.service.text import normalize

_CATALOG: Path = settings.CATALOG_PATH

_COL_RE = re.compile(r"наимен", re.I)  # столбец «НАИМЕНОВАНИЕ»
_CELL_RE = re.compile(r"наимен", re.I)

# ────────────────────────── кеш ───────────────────────────
_cache: Set[str] | None = None  # набор префиксов
_lock = asyncio.Lock()  # защита от гонок


def _prefixes(text: str, n: int = 5) -> Set[str]:
    return {tok[:n] for tok in text.split() if len(tok) >= n}


def _detect_header() -> int:
    preview = pd.read_excel(
        _CATALOG, sheet_name=0, engine="pyxlsb", header=None, nrows=10
    )
    for idx, row in preview.iterrows():
        if any(_CELL_RE.search(str(c)) for c in row):
            return idx
    raise ValueError("Строка шапки с «НАИМЕНОВАНИЕ» не найдена")


def _load_once() -> Set[str]:
    """
    Синхронное чтение XLSB → множество префиксов.
    Вызывается только из потока ThreadPoolExecutor.
    """
    hdr = _detect_header()
    df = pd.read_excel(_CATALOG, sheet_name=0, engine="pyxlsb", header=hdr)
    name_col = next(c for c in df.columns if _COL_RE.search(str(c)))

    pref_set: set[str] = set()
    for raw in df[name_col].dropna().astype(str):
        pref_set.update(_prefixes(normalize(raw)))

    logger.info("Каталог загружен: {} префиксов", len(pref_set))
    return pref_set


async def load_catalog(force: bool = False) -> Set[str]:
    """
    Возвращает кешированный набор префиксов.
    * при первом вызове читает XLSB в отдельном треде;
    * последующие вызовы — мгновенный возврат кеша;
    * `force=True` перечитывает каталог (можно дергать из админ-команды).
    """
    global _cache
    async with _lock:
        if _cache is None or force:
            _cache = await asyncio.to_thread(_load_once)
        return _cache


# helper для unit-тестов
def sync() -> Set[str]:
    return asyncio.run(load_catalog())


__all__ = ["load_catalog", "sync"]
