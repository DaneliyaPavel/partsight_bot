from bot.service.text import normalize


def test_normalize_basic():
    assert normalize("Форсунка 5258744 Movelex") == "5258744 форсунка"
    # pymorphy2 лемматизирует «ремня» → «ремень»
    assert normalize("НАТЯЖНОЙ  ролик ремня") == "натяжной ролик ремень"
