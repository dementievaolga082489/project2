from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, "USD")

    Returns:
        Итератор, выдающий транзакции с указанной валютой
    """
    for transaction in transactions:
        # Проверяем наличие структуры operationAmount и currency
        if (
            transaction.get("operationAmount")
            and transaction["operationAmount"].get("currency")
            and transaction["operationAmount"]["currency"].get("code") == currency
        ):
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """
    Генерирует описания транзакций.

    Args:
        transactions: Список словарей с транзакциями

    Returns:
        Генератор, выдающий описания транзакций
    """
    for transaction in transactions:
        if transaction.get("description"):
            yield transaction["description"]


def card_number_generator(start: int, end: int) -> Generator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX

    Args:
        start (int): начальное значение диапазона (от 1 до 9999 9999 9999 9999)
        end (int): конечное значение диапазона (от 1 до 9999 9999 9999 9999)

    Yields:
        str: номер карты в формате "XXXX XXXX XXXX XXXX"
    """
    for number in range(start, end + 1):
        # Преобразуем число в строку
        number_str = str(number)

        # Добавляем ведущие нули вручную до 16 цифр
        zeros_needed = 16 - len(number_str)
        card_number = "0" * zeros_needed + number_str

        # Форматируем строку: XXXX XXXX XXXX XXXX
        formatted_number = f"{card_number[0:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"

        yield formatted_number
