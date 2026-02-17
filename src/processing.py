from typing import Any


def filter_by_state(transactions: list[dict[str, Any]], state: str = 'EXECUTED') -> list[dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    result = []
    for char in transactions:
        if char.get('state') == state:
            result.append(char)
    return result


def sort_by_date(records: list[dict], descending: bool = True) -> list[dict]:
    """
    Принимает список словарей и необязательный параметр, задающий порядок
    сортировки (по умолчанию — убывание). Функция должна возвращать новый список,
     отсортированный по дате.
     """

    sorted_list = sorted(records, key=lambda x: x['date'], reverse=descending)
    return sorted_list
