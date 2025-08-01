from __future__ import annotations

from typing import Set

from .text import normalize


def can_produce(raw_name: str, catalog_pref: Set[str]) -> bool:
    """
    «Да», если хотя бы один 5-символьный префикс леммы из запроса
    встречается среди префиксов каталога.
    """
    q_pref = {tok[:5] for tok in normalize(raw_name).split() if len(tok) >= 5}
    return bool(q_pref & catalog_pref)


__all__ = ["can_produce"]
