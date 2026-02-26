from typing import Any, List, Tuple

import pytest

from src.widget import get_date, mask_account_card


def test_mixed_data_from_fixture(mixed_test_data: List[Tuple[str, str]]) -> None:
    """Проверка смешанных данных из фикстуры"""
    for info, expected in mixed_test_data:
        assert mask_account_card(info) == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",  # пустая строка
        "   ",  # только пробелы
        "Visa Platinum",  # без номера
        "MasterCard",  # без номера
        "Счет",  # без номера
        "Visa Platinum abc",  # номер не цифрами
        "Счет abc",  # номер не цифрами
        "Счет 12",  # слишком короткий номер
    ],
)
def test_invalid_inputs_return_original(invalid_input: str) -> None:
    """Некорректные входные данные возвращаются без изменений"""
    result = mask_account_card(invalid_input)
    assert result == invalid_input


@pytest.mark.parametrize(
    "non_string_input",
    [
        123456789,  # целое число
        12345.67,  # число с плавающей точкой
        [1, 2, 3],  # список
        (1, 2, 3),  # кортеж
        {"key": "value"},  # словарь
        True,  # булево значение
        False,  # булево значение
        b"bytes string",  # байтовая строка
        None,  # None (уже есть отдельный тест)
    ],
)
def test_non_string_inputs_return_original(non_string_input: Any) -> None:
    """Тест не-строковые типы данных возвращаются без изменений"""
    result = mask_account_card(non_string_input)
    assert result == non_string_input


@pytest.mark.parametrize(
    "input_date,expected",
    [
        ("2024-01-01T00:00:00", "01.01.2024"),
        ("2024-12-31T23:59:59", "31.12.2024"),
        ("2024-02-28T12:00:00", "28.02.2024"),
    ],
)
def test_parametrized_dates(input_date: str, expected: str) -> None:
    """Тестирование правильности преобразования даты"""
    assert get_date(input_date) == expected


def test_invalid_dates_with_fixture(invalid_date_strings: List[Tuple[str, str]]) -> None:
    """Тест невалидных дат с использованием фикстуры"""
    for date_str, description in invalid_date_strings:
        result = get_date(date_str)
        assert "Ошибка" in result, f"Должна быть ошибка для {description}: {date_str}"


def test_empty_strings_with_fixture(empty_strings: List[Tuple[str, str]]) -> None:
    """Тест пустых строк с использованием фикстуры"""

    expected = "Ошибка: пустая строка или некорректный тип данных"

    for input_str, description in empty_strings:
        result = get_date(input_str)
        assert result == expected, f"Для '{description}' ожидалось: {expected}"


def test_non_string_inputs_with_fixture(non_string_inputs: List[Tuple[Any, str]]) -> None:
    """Тест нестроковых типов с использованием фикстуры"""

    expected = "Ошибка: пустая строка или некорректный тип данных"

    for input_value, description in non_string_inputs:
        result = get_date(input_value)
        assert result == expected, f"Для {description} ожидалось: {expected}"


def test_date_components_count() -> None:
    """Тест для проверки количества компонентов даты (должно быть 3)"""

    test_cases: List[Tuple[str, str]] = [
        # Меньше 3 компонентов
        ("2024", "только год"),
        ("2024-03", "год и месяц"),
        ("2024-03-", "год и месяц с дефисом в конце"),
        ("2024-", "год с дефисом"),
        ("-2024", "дефис в начале"),
        # Больше 3 компонентов
        ("2024-03-11-extra", "дополнительный компонент"),
        ("2024-03-11-12-30", "несколько дополнительных компонентов"),
        # Специальные случаи
        ("----", "только дефисы"),
        ("---", "три дефиса"),
        ("2024--03-11", "пустой компонент между дефисами"),
        ("2024-03--11", "пустой компонент"),
    ]

    expected_error = "Ошибка: неверный формат даты"

    for input_str, description in test_cases:
        result = get_date(input_str)

        assert result == expected_error, f"Для '{description}' ожидалось: {expected_error}, получено: {result}"


@pytest.mark.parametrize(
    "input_str, description, expected_error",
    [
        # Буквы в разных компонентах
        ("abcd-03-11", "буквы в году", "Ошибка: компоненты даты должны быть числами"),
        ("abcd-ef-gh", "буквы во всех компонентах", "Ошибка: компоненты даты должны быть числами"),
        # Смешанные буквы и цифры
        ("2024-03-11c", "буква после цифр в дне", "Ошибка: компоненты даты должны быть числами"),
        ("a2024-03-11", "буква перед цифрами в году", "Ошибка: компоненты даты должны быть числами"),
        # Специальные символы
        ("2024-@03-11", "спецсимвол @ в месяце", "Ошибка: компоненты даты должны быть числами"),
        ("2024-03-#11", "спецсимвол # в дне", "Ошибка: компоненты даты должны быть числами"),
        ("2024-03-+11", "спецсимвол + в дне", "Ошибка: компоненты даты должны быть числами"),
        # Знаки препинания
        ("2024:03:11", "двоеточия", "Ошибка: неверный формат даты"),
        ("2024!03!11", "восклицательные знаки", "Ошибка: неверный формат даты"),
        ("2024?03?11", "вопросительные знаки", "Ошибка: неверный формат даты"),
    ],
)
def test_non_digit_components_parametrized(input_str: str, description: str, expected_error: str) -> None:
    """Параметризованный тест для нецифровых компонентов"""
    result = get_date(input_str)

    assert (
        result == expected_error or expected_error in result
    ), f"Для '{description}' ожидалось: {expected_error}, получено: {result}"
