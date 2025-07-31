from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def mini_catalog(tmp_path: Path) -> Path:
    """
    Генерирует маленький каталог и сохраняет как .xlsx.
    (writer openpyxl доступен у pandas по умолчанию, если установлен пакет)
    """
    data = {
        "CatalogID": [1, 2, 3],
        "НАИМЕНОВАНИЕ": [
            "Форсунка топливная высокого давления",
            "Натяжной ролик ремня привода",
            "Хомут стяжной 50-70 мм",
        ],
    }
    df = pd.DataFrame(data)
    file = tmp_path / "mini.xlsx"
    df.to_excel(file, index=False)  # <-- без engine="pyxlsb"
    return file
