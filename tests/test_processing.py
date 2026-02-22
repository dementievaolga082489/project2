from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
    ],
)
def test_filter_by_different_state(
    transactions: List[Dict[str, Any]], state: str, expected: List[Dict[str, Any]]
) -> None:
    """Тестирование фильтрации списка словарей по заданному статусу state"""

    filtered = filter_by_state(transactions, state)
    assert filtered == expected


def test_filter_by_nonexistent_state(transactions: List[Dict[str, Any]]) -> None:
    """Тестирование фильтрации по статусу, отсутствующему в списке"""
    # Пытаемся отфильтровать по несуществующему статусу
    filtered = filter_by_state(transactions, "PENDING")

    # Ожидаем пустой список
    assert filtered == []
    assert isinstance(filtered, list)


@pytest.mark.parametrize(
    "state", ["PENDING", "PROCESSING", "COMPLETED", "UNKNOWN", "     ", ""]  # строка с пробелами  # пустая строка
)
def test_filter_by_various_nonexistent_states(transactions: List[Dict[str, Any]], state: str) -> None:
    """Параметризованный тест для различных несуществующих статусов"""
    filtered = filter_by_state(transactions, state)
    assert filtered == []


@pytest.mark.parametrize(
    "reverse_order, expected",
    [
        (
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-09-12T08:21:33.419441"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),  # Убывающий порядок
        (
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-09-12T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),  # Возрастающий порядок
    ],
)
def test_sort_by_date_order(
    operations: List[Dict[str, Any]], reverse_order: bool, expected: List[Dict[str, Any]]
) -> None:
    """Тестирование сортировки списка словарей по датам в порядке убывания и возрастания."""
    sorted_operations = sort_by_date(operations, reverse_order)
    assert sorted_operations == expected


def test_invalid_input_type() -> None:
    """Тест: передача не списка должна вызывать ValueError"""
    with pytest.raises(ValueError) as exc_info:
        sort_by_date("not a list")  # type: ignore[arg-type]
    assert "Дата должна быть строкой, получен <class 'str'>" in str(exc_info.value)


def test_empty_list() -> None:
    """Тест: передача пустого списка должна вызывать ValueError"""
    with pytest.raises(ValueError) as exc_info:
        sort_by_date([])
    assert "Пустая строка даты" in str(exc_info.value)
