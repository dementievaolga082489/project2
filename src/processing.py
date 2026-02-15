from typing import Any


def filter_by_state(list_dict: list[dict[str, Any]], state: str = 'EXECUTED') -> list[dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    new_dict = []
    for i in list_dict:
        if i.get('state') == state:
            new_dict.append(i)
    return new_dict


def sort_by_date(list_dict: list[dict], descending: bool = True) -> list[dict]:
    """
    Принимает список словарей и необязательный параметр, задающий порядок
    сортировки (по умолчанию — убывание). Функция должна возвращать новый список,
     отсортированный по дате.
     """

    sorted_list = sorted(list_dict, key=lambda x: x['date'], reverse=descending)
    return sorted_list
