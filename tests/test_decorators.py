import pytest

from src.decorators import log


def test_successful_execution_console(capsys):
    """Тест успешного выполнения функции с выводом в консоль"""

    @log()
    def add(a, b):
        return a + b

    result = add(5, 3)

    # Проверяем результат функции
    assert result == 8

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "add ok. Result: 8" in captured.out


def test_error_execution_console(capsys):
    """Тест выполнения функции с ошибкой и выводом в консоль"""

    @log()
    def divide(a, b):
        return a / b

    # Проверяем, что исключение пробрасывается дальше
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError. Inputs: (10, 0), {}" in captured.out


def test_successful_execution_file(log_filename):
    """Тест успешного выполнения функции с записью в файл"""

    @log(filename=log_filename)
    def subtract(a, b):
        return a - b

    result = subtract(10, 4)

    assert result == 6

    # Проверяем содержимое файла
    with open(log_filename, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == "subtract ok. Result: 6"


def test_error_execution_file(log_filename):
    """Тест выполнения функции с ошибкой и записью в файл"""

    @log(filename=log_filename)
    def get_item(lst, index):
        return lst[index]

    with pytest.raises(IndexError):
        get_item([1, 2, 3], 5)

    # Проверяем содержимое файла
    with open(log_filename, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert "get_item error: IndexError. Inputs: ([1, 2, 3], 5), {}" in content
