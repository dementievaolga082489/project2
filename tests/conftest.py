from typing import Any, Dict, List, Optional, Tuple

import pytest


# Фикстура для модуля widget.py функции mask_account_card
@pytest.fixture
def mixed_test_data() -> List[Tuple[str, str]]:
    """Фикстура со смешанными данными"""
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro Premium 1596837868705199", "Maestro Premium 1596 83** **** 5199"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ]


# Фикстура для модуля widget.py функции get_date
@pytest.fixture
def invalid_date_strings() -> List[Tuple[Optional[str], str]]:
    """Фикстура с невалидными строками дат"""
    return [
        ("", "пустая строка"),
        (None, "None значение"),
        ("2024-13-01", "неверный месяц"),
        ("2024-00-15", "нулевой месяц"),
        ("2024-02-30T10:30:00", "30 февраля"),
        ("2023-02-29", "29 февраля в обычный год"),
        ("2024-04-31", "31 апреля"),
        ("2024-02-29T", "обрезанная дата"),
        ("2024-08-32", "32 августа"),
    ]


# Фикстура для модуля widget.py функции get_date
@pytest.fixture
def empty_strings() -> List[Tuple[str, str]]:
    """Фикстура с различными пустыми строками"""
    return [
        ("", "абсолютно пустая строка"),
        (" ", "один пробел"),
        ("  ", "два пробела"),
        ("   ", "три пробела"),
        ("\t", "табуляция"),
        ("\n", "новая строка"),
    ]


# Фикстура для модуля widget.py функции get_date
@pytest.fixture
def non_string_inputs() -> List[Tuple[Any, str]]:
    """Фикстура с различными нестроковыми типами"""
    return [
        (123, "целое число"),
        (123456789, "большое целое"),
        (-42, "отрицательное число"),
        (0, "ноль"),
        (3.14159, "число с плавающей точкой"),
        (1.23e-4, "экспоненциальная запись"),
        (True, "булево True"),
        (False, "булево False"),
        ([1, 2, 3], "список чисел"),
        (["a", "b", "c"], "список строк"),
        ([None], "список с None"),
    ]


# Фикстура для модуля processing.py для функции filter_by_state
@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    """Фикстура с данными для проверки фильтрации по 'state'"""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


# Фикстура для модуля processing.py для функции sort_by_date
@pytest.fixture
def operations() -> List[Dict[str, Any]]:
    """Фикстура с данными для проверки сортировки"""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-09-12T08:21:33.419441"},  # Одинаковая дата
    ]


# Фикстура для модуля generators
@pytest.fixture
def transactions_():
    return [
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
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
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
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


# Фикстура для модуля decorates.py
@pytest.fixture
def log_filename(tmp_path):
    """Фикстура для создания временного файла лога"""
    return str(tmp_path / "test.log")


# Фикстуры для модуля external.api
@pytest.fixture
def usd_transaction() -> Dict[str, Any]:
    """Фикстура для транзакции в долларах"""
    return {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}


@pytest.fixture
def rub_transaction() -> Dict[str, Any]:
    """Фикстура для транзакции в рублях"""
    return {"operationAmount": {"amount": "1000.50", "currency": {"code": "RUB"}}}
