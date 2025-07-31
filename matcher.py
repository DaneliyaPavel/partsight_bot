from utils import normalize

def can_produce(raw_name: str,
                catalog_pref: set[str]) -> bool:
    """ДА, если хотя бы один 5-символьный префикс из запроса
       встречается в наборе префиксов каталога."""
    q_pref = {tok[:5] for tok in normalize(raw_name).split() if len(tok) >= 5}
    return bool(q_pref & catalog_pref)
