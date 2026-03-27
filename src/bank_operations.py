import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, str]]:
    """
     Принимает список словарей с данными о банковских операциях и строку поиска,
    и возвращает список словарей, у которых в описании есть данная строка.
    """

    lst_transactions = []
    for transaction in data:
        if transaction.get("description", ""):
            if re.search(search, transaction.get("description", ""), flags=re.IGNORECASE):
                lst_transactions.append(transaction)
    return lst_transactions


test_data = [
    {
        "id": 3598919.0,
        "state": "EXECUTED",
        "date": "2020-12-06T23:00:58Z",
        "amount": [29740.0],
        "currency_name": "Peso",
        "currency_code": "COP",
        "from": "Discover 3172601889670065",
        "to": "Discover 0720428384694643",
        "description": "Перевод с карты на карту",
    }
]
print(process_bank_search(test_data, "Перевод с карты на карту"))


def process_bank_operations(data: List[Dict[str, str]], categories: List[str]) -> Dict[str, int]:
    """
     Принимает список словарей с данными о банковских операциях и список категорий операций, и возвращает словарь,
    в котором ключи — это названия категорий, а значения — это количество операций в каждой категории.
    """
    count = Counter({category: 0 for category in categories})

    for dict_item in data:
        description = dict_item.get("description", "").lower()
        for category in categories:
            if re.search(category.lower(), description):
                count[category] += 1
    return dict(count)


test_data_ = [
    {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    },
    {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
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
categories = ["Перевод организации", "Перевод с карты на карту"]
result = process_bank_operations(test_data_, categories)
print(result)
