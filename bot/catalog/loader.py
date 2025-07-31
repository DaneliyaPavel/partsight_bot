from __future__ import annotations

import asyncio
import re
from pathlib import Path
from typing import Set

import pandas as pd

from bot.config import settings
from bot.utils.text import normalize

_CATALOG: Path = settings.CATALOG_PATH

_COL_RE = re.compile(r"наимен", re.I)  # столбец «НАИМЕНОВАНИЕ»
_CELL_RE = re.compile(r"наимен", re.I)  # ищем в первых строках


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


async def load_catalog() -> Set[str]:
    """Читает каталог и отдаёт набор всех 5-символьных префиксов лемм."""

    def _read() -> Set[str]:
        hdr = _detect_header()
        df = pd.read_excel(_CATALOG, sheet_name=0, engine="pyxlsb", header=hdr)
        name_col = next(c for c in df.columns if _COL_RE.search(str(c)))

        pref_set: set[str] = set()
        for raw in df[name_col].dropna().astype(str):
            pref_set.update(_prefixes(normalize(raw)))
        return pref_set

    return await asyncio.to_thread(_read)


# helper для unit-тестов
def sync() -> Set[str]:
    import asyncio

    return asyncio.run(load_catalog())


__all__ = ["load_catalog", "sync"]
