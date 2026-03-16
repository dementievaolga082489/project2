from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import get_convert


# Параметризованные тесты для конвертации рублей
@pytest.mark.parametrize(
    "amount, expected",
    [
        ("1000.50", 1000.50),
        ("0.00", 0.00),
        ("500", 500.0),
        ("1234.56", 1234.56),
    ],
)
def test_get_convert_rub(amount: str, expected: float, rub_transaction) -> None:
    """Тест прямой конвертации RUB (без вызова API)"""
    rub_transaction["operationAmount"]["amount"] = amount
    result = get_convert(rub_transaction)
    assert result == expected
    assert isinstance(result, float)


# Параметризованные тесты для успешной конвертации валют
@pytest.mark.parametrize(
    "currency, amount, converted_amount",
    [
        ("USD", "100.00", 7500.00),
        ("USD", "50.50", 3787.50),
        ("EUR", "100.00", 8500.00),
        ("EUR", "75.25", 6396.25),
    ],
)
@patch("requests.get")
def test_get_convert_success(mock_get, currency, amount, converted_amount) -> None:
    """Тест успешной конвертации различных валют с разными суммами"""

    transaction = {"operationAmount": {"amount": amount, "currency": {"code": currency}}}

    # Настраиваем мок-ответ
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"result": converted_amount}
    mock_get.return_value = mock_response

    # Вызываем функцию
    result = get_convert(transaction)

    # Проверяем результат
    assert result == converted_amount
    assert isinstance(result, float)

    # Проверяем, что запрос был сделан с правильными параметрами
    mock_get.assert_called_once()


# Параметризованные тесты для различных ошибок API
@pytest.mark.parametrize(
    "exception, expected_result",
    [
        (requests.exceptions.HTTPError("404 Not Found"), 0.0),
        (requests.exceptions.ConnectionError("Connection failed"), 0.0),
        (requests.exceptions.Timeout("Request timeout"), 0.0),
        (requests.exceptions.RequestException("General error"), 0.0),
        (Exception("Unexpected error"), Exception),
    ],
)
@patch("requests.get")
def test_convert_api_errors(mock_get, exception, expected_result, usd_transaction) -> None:
    """Тест обработки различных ошибок API"""
    mock_get.side_effect = exception

    # Проверяем, является ли expected_result классом Exception
    if expected_result is Exception:
        # Ожидаем, что будет выброшено исключение
        with pytest.raises(Exception) as exc_info:
            get_convert(usd_transaction)
        # Проверяем сообщение исключения
        assert str(exc_info.value) == "Unexpected error"
    else:
        result = get_convert(usd_transaction)
        assert result == expected_result
