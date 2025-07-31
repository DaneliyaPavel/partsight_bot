import pandas as pd, asyncio, configparser, re
from pathlib import Path
from utils import normalize

_cfg = configparser.ConfigParser(); _cfg.read("config.ini")
_CATALOG = Path(_cfg["files"]["CATALOG_PATH"])

_FIND_COL = re.compile(r"наимен", re.I)   # ищем в названии столбца
_FIND_CELL = re.compile(r"наимен", re.I)  # ищем в ячейках первых строк

def _prefixes(text: str, n: int = 5) -> set[str]:
    return {tok[:n] for tok in text.split() if len(tok) >= n}

def _detect_header() -> int:
    """Возвращает индекс строки (0-based), где расположена шапка."""
    # читаем первые 10 строк без заголовка
    preview = pd.read_excel(_CATALOG, sheet_name=0,
                            engine="pyxlsb", header=None, nrows=10)
    for idx, row in preview.iterrows():
        if any(_FIND_CELL.search(str(cell)) for cell in row):
            return idx
    raise ValueError("Не нашёл строку с «НАИМЕНОВАНИЕ» в первых 10 строках")

async def load_catalog() -> set[str]:
    """Возвращает набор префиксов (5-букв) всех лемм каталога."""
    def _read():
        hdr = _detect_header()
        df = pd.read_excel(_CATALOG, sheet_name=0,
                           engine="pyxlsb", header=hdr)
        name_col = next(c for c in df.columns if _FIND_COL.search(str(c)))

        pref_set: set[str] = set()
        for raw in df[name_col].dropna().astype(str):
            pref_set.update(_prefixes(normalize(raw)))
        return pref_set
    return await asyncio.to_thread(_read)
