from bot.service.matcher import can_produce


def test_matcher_positive():
    # 5-символьные префиксы!
    pref = {"форсу", "натяж", "ролик"}
    assert can_produce("Форсунка 5258744", pref)
    assert can_produce("Натяжитель ремня", pref)
    assert can_produce("Ролик натяжителя ГРМ", pref)


def test_matcher_negative_basic():
    pref = {"форсу"}
    assert not can_produce("Прокладка ГБЦ", pref)
    assert not can_produce("Сальник полуоси", pref)


def test_matcher_negative_exotic():
    pref = {"форсу", "натяж", "ролик"}
    exotic_items = [
        "Турбина Tesla Model ≠",
        "Редуктор шаурмобота",
        "Квантовый фланец высоких энергий",
        "Стабилизатор гиперпространства",
        "Гарпун для ловли комет",
    ]
    for item in exotic_items:
        assert not can_produce(item, pref)
