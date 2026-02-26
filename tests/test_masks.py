import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_not_string() -> None:
    """Тест: передача числа вместо строки должна вызывать ошибку"""
    with pytest.raises(ValueError) as excinfo:
        get_mask_card_number(1234567890123456)  # type: ignore[arg-type]   # передаем int

    assert str(excinfo.value) == "Номер карты должен быть строкой"


# Параметризация теста
@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("1111222233334444", "1111 22** **** 4444"),
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "invalid_card_number, expected_error",
    [
        ("123", "Номер карты должен содержать 16 цифр"),  # короткий номер
        ("12345678901234567", "Номер карты должен содержать 16 цифр"),  # длинный номер
        ("1234abcd5678efgh", "Номер карты должен содержать только цифры"),  # символы
        ("", "Номер карты должен содержать 16 цифр"),  # пустая строка
    ],
)
def test_get_mask_card_number_invalid(invalid_card_number: str, expected_error: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(invalid_card_number)
    assert str(exc_info.value) == expected_error


@pytest.mark.parametrize(
    "invalid_input,expected_message",
    [
        ("", "Номер счета не может быть пустым"),
        ("1", "Номер счета должен содержать минимум 4 символа"),
    ],
)
def test_error_messages(invalid_input: str, expected_message: str) -> None:
    """Проверка текста сообщений об ошибках"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(invalid_input)
    assert expected_message in str(exc_info.value)


@pytest.mark.parametrize(
    "account,expected",
    [("73654108430135874305", "**4305"), ("1234567890123456", "**3456"), ("12345", "**2345"), ("1234", "**1234")],
)
def test_mask_valid_accounts(account: str, expected: str) -> None:
    """Тест правильности маскирования счета"""
    assert get_mask_account(account) == expected
