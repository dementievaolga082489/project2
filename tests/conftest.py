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
