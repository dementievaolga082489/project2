from src.bank_operations import process_bank_operations, process_bank_search


def test_search_exact_match(transactions_):
    """Тест: точное совпадение с описанием"""

    result = process_bank_search(transactions_, "Перевод с карты на карту")
    assert len(result) == 1
    assert result[0]["description"] == "Перевод с карты на карту"


def test_search_no_match(transactions_):
    """Тест: нет совпадений"""

    result = process_bank_search(transactions_, "Покупка")
    assert len(result) == 0


def test_count_single_category(transactions_):
    """Тест: подсчет операций по категории"""
    categories = ["Перевод организации"]
    result = process_bank_operations(transactions_, categories)
    assert result == {"Перевод организации": 2}


def test_category_not_found(transactions_):
    """Тест: категория не найдена"""

    categories = ["Покупка", "Оплата ЖКХ"]
    result = process_bank_operations(transactions_, categories)
    assert result == {"Покупка": 0, "Оплата ЖКХ": 0}
