from unittest.mock import mock_open, patch

from src.utils import read_json_file

mock_file = mock_open(
    read_data='[{"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041",'
    ' "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},'
    ' "description": "Перевод организации", "from": "Maestro 1596837868705199", "to": "Счет 64686473678894779589"}]'
)


# Тест на проверку работы функции
@patch("builtins.open", mock_file)
def test_read_json_file_success() -> None:
    with patch(
        "json.load", return_value=[{"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"}]
    ) as mock_load:
        result = read_json_file("./data/operations.json")

        # Проверяем, что json.load действительно был вызван
        mock_load.assert_called_once()

        assert result == [{"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"}]


# Тест, если файл пуст
@patch("builtins.open", mock_file)
def test_read_json_file_empty() -> None:
    with patch("json.load", return_value=None) as mock_load:
        result = read_json_file("./data/operations.json")

        # Проверяем, что json.load был вызван
        mock_load.assert_called_once()

        assert result == []


@patch("builtins.open", mock_file)
def test_read_json_file_not_list() -> None:
    """Тест: файл содержит словарь вместо списка"""
    with patch(
        "json.load",
        return_value={
            "id": 441945886,
            "state": "EXECUTED",
            # ... остальные поля
        },
    ) as mock_load:
        result = read_json_file("./data/operations.json")

        # Проверяем, что json.load действительно был вызван
        mock_load.assert_called_once()

        assert result == []


def test_read_json_file_file_not_found() -> None:
    """Тест: файл не найден (должен вернуть пустой список)"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_json_file("./data/nonexistent.json")
        assert result == []
