from unittest.mock import patch

import pandas as pd
import pytest

from src.transaction_reader import reader_csv_file, reader_excel_file


@patch("pandas.read_csv")
def test_success_readr_csv(mock_read_csv):
    """Тест успешного чтения CSV файла"""
    test_data = {
        "id": [3598919.0],
        "state": ["EXECUTED"],
        "date": ["2020-12-06T23:00:58Z"],
        "amount": [29740.0],
        "currency_name": ["Peso"],
        "currency_code": ["COP"],
        "from": ["Discover 3172601889670065"],
        "to": ["Discover 0720428384694643"],
        "description": ["Перевод с карты на карту"],
    }

    # Создаем DataFrame из test_data
    mock_read_csv.return_value = pd.DataFrame(test_data)

    # Ожидаемый результат
    expected_result = [
        {
            "id": 3598919.0,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740.0,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        }
    ]
    # Вызываем функцию и проверяем результат
    result = reader_csv_file("fake_path.csv")
    assert result == expected_result
    # Проверяем, что функция вызвана с правильным аргументом
    mock_read_csv.assert_called_once_with("fake_path.csv", sep=";")


@patch("pandas.read_csv")
def test_file_not_found_csv(mock_read_csv):
    """Тест ситуации, когда CSV файл не найден"""
    # Подготовка
    mock_read_csv.side_effect = FileNotFoundError("Файл не найден")

    # Действие и проверка
    with pytest.raises(FileNotFoundError) as exc_info:
        reader_csv_file("несуществующий/файл.csv")

    assert "Файл не найден по пути несуществующий/файл.csv" in str(exc_info.value)
    mock_read_csv.assert_called_once_with("несуществующий/файл.csv", sep=";")


@patch("pandas.read_csv")
def test_value_error_csv(mock_read_csv):
    """Тест ошибки при чтении некорректного CSV файла"""
    # Подготовка
    mock_read_csv.side_effect = ValueError("Некорректный формат CSV")

    # Действие и проверка
    with pytest.raises(ValueError) as exc_info:
        reader_csv_file("некорректный/файл.csv")

    assert "Ошибка при чтении файла CSV: Некорректный формат CSV" in str(exc_info.value)
    mock_read_csv.assert_called_once_with("некорректный/файл.csv", sep=";")


@patch("pandas.read_excel")
def test_success_readr_xlsx(mock_read_xlsx):
    """Тест успешного чтения EXCEL файла"""
    test_df = {
        "id": [650703.0],
        "state": ["EXECUTED"],
        "date": ["2023-09-05T11:30:32Z"],
        "amount": [16210.0],
        "currency_name": ["Sol"],
        "currency_code": ["PEN"],
        "from": ["Счет 58803664561298323391"],
        "to": ["Счет 39745660563456619397"],
        "description": ["Перевод организации"],
    }

    # Создаем DataFrame из test_df
    mock_read_xlsx.return_value = pd.DataFrame(test_df)

    # Ожидаемый результат
    expected_result = [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
    ]
    # Вызываем функцию и проверяем результат
    result = reader_excel_file("fake_path.xlsx")
    assert result == expected_result
    # Проверяем, что функция вызвана с правильным аргументом
    mock_read_xlsx.assert_called_once_with("fake_path.xlsx")


@patch("pandas.read_excel")
def test_file_not_found_xlsx(mock_read_xlsx):
    """Тест ситуации, когда EXCEL файл не найден"""
    # Подготовка
    mock_read_xlsx.side_effect = FileNotFoundError("Файл не найден")

    # Действие и проверка
    with pytest.raises(FileNotFoundError) as exc_info:
        reader_excel_file("несуществующий/файл.xlsx")

    assert "Файл не найден по пути несуществующий/файл.xlsx" in str(exc_info.value)
    mock_read_xlsx.assert_called_once_with("несуществующий/файл.xlsx")


@patch("pandas.read_excel")
def test_value_error_xlsx(mock_read_xlsx):
    """Тест ошибки при чтении некорректного EXCEL файла"""
    # Подготовка
    mock_read_xlsx.side_effect = ValueError("Некорректный формат XLSX")

    # Действие и проверка
    with pytest.raises(ValueError) as exc_info:
        reader_excel_file("некорректный/файл.xlsx")

    assert "Ошибка при чтении файла Excel: Некорректный формат XLSX" in str(exc_info.value)
    mock_read_xlsx.assert_called_once_with("некорректный/файл.xlsx")
