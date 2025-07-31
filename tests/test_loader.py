import pandas as pd
from bot.catalog import loader
from bot.config import settings


def test_loader_prefixes(mini_catalog, monkeypatch):
    """
    Подменяем путь к каталогу на мини-файл .xlsx и отбрасываем
    аргумент engine внутри pandas.read_excel.
    """
    monkeypatch.setattr(settings, "CATALOG_PATH", mini_catalog)

    original_read_excel = pd.read_excel

    def _patched(*args, **kwargs):
        kwargs.pop("engine", None)  # игнорируем pyxlsb
        return original_read_excel(*args, **kwargs)

    monkeypatch.setattr(loader.pd, "read_excel", _patched)

    pref_set = loader.sync()
    assert "форсу" in pref_set
    assert "натяж" in pref_set
    assert "хомут" in pref_set
