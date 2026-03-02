import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize(
    "currency, expected",
    [
        (
            "USD",
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
                {
                    "id": 895315941,
                    "state": "EXECUTED",
                    "date": "2018-08-19T04:27:37.904916",
                    "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод с карты на карту",
                    "from": "Visa Classic 6831982476737658",
                    "to": "Visa Platinum 8990922113665229",
                },
            ],
        ),
        (
            "RUB",
            [
                {
                    "id": 873106923,
                    "state": "EXECUTED",
                    "date": "2019-03-23T01:09:46.296404",
                    "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                },
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                    "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод организации",
                    "from": "Visa Platinum 1246377376343588",
                    "to": "Счет 14211924144426031657",
                },
            ],
        ),
        ("EUR", []),
    ],
)
def test_filter_by_different_currencies(transactions_, currency, expected):
    """Проверка фильтрации по разным валютам"""

    result = list(filter_by_currency(transactions_, currency))
    assert result == expected


def test_filter_by_empty_transactions():
    """Проверка по пустому списку"""
    empty_transactions = []
    expected = []
    # тест
    assert list(filter_by_currency(empty_transactions, "USD")) == expected


def test_transaction_descriptions_all_descriptions(transactions_):
    """Проверяет, что функция возвращает все описания транзакций"""
    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]

    result = list(transaction_descriptions(transactions_))
    assert result == expected_descriptions


@pytest.mark.parametrize(
    "transactions, expected_descriptions",
    [
        # Тест 1: Пустой список
        ([], []),
        # Тест 2: Одна транзакция с описанием
        ([{"id": 1, "description": "Перевод организации"}], ["Перевод организации"]),
        # Тест 3: Несколько транзакций с описаниями
        (
            [
                {"id": 1, "description": "Перевод организации"},
                {"id": 2, "description": "Перевод со счета на счет"},
                {"id": 3, "description": "Перевод с карты на карту"},
            ],
            ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"],
        ),
    ],
)
def test_transaction_descriptions_basic_cases(transactions, expected_descriptions):
    """Базовые тесты с различным количеством транзакций"""
    result = list(transaction_descriptions(transactions))
    assert result == expected_descriptions


@pytest.mark.parametrize(
    "transactions, expected_descriptions",
    [
        # Тест 1: Транзакция без поля description
        ([{"id": 1, "amount": "100"}], []),
        # Тест 2: Транзакция с пустым описанием
        ([{"id": 1, "description": ""}], []),
        # Тест 3: Смешанные транзакции (с описанием и без)
        (
            [
                {"id": 1, "description": "Перевод"},
                {"id": 2, "amount": "500"},
                {"id": 3, "description": ""},
                {"id": 4, "description": "Оплата"},
            ],
            ["Перевод", "Оплата"],
        ),
        # Тест 4: Транзакции с None в description
        (
            [{"id": 1, "description": "Перевод"}, {"id": 2, "description": None}, {"id": 3, "description": "Оплата"}],
            ["Перевод", "Оплата"],
        ),
    ],
)
def test_transaction_descriptions_edge_cases(transactions, expected_descriptions):
    """Тесты с граничными случаями (отсутствие описания, пустое описание, None)"""
    result = list(transaction_descriptions(transactions))
    assert result == expected_descriptions


# Тесты для функции card_number_generator
@pytest.mark.parametrize(
    "start, end, expected",
    [
        # Базовые тесты
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (100, 102, ["0000 0000 0000 0100", "0000 0000 0000 0101", "0000 0000 0000 0102"]),
        # Тесты с разными количествами ведущих нулей
        (5, 5, ["0000 0000 0000 0005"]),
        (1000000, 1000002, ["0000 0000 0100 0000", "0000 0000 0100 0001", "0000 0000 0100 0002"]),
        # Тесты с нулевым начальным значением
        (0, 2, ["0000 0000 0000 0000", "0000 0000 0000 0001", "0000 0000 0000 0002"]),
        # Тесты с большими числами
        (9999999999999997, 9999999999999999, ["9999 9999 9999 9997", "9999 9999 9999 9998", "9999 9999 9999 9999"]),
        # Тест с диапазоном из одного элемента
        (1234567890123456, 1234567890123456, ["1234 5678 9012 3456"]),
    ],
)
def test_card_number_generator_parametrized(start, end, expected):
    """Параметризованный тест для различных диапазонов"""
    generator = card_number_generator(start, end)
    result = list(generator)
    assert result == expected
    assert len(result) == len(expected)
