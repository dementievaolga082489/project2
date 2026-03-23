from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

SRC_DIR = Path(__file__).resolve().parent

DATA_DIR = SRC_DIR.parent / "data"

CSV_FILE = DATA_DIR / "transactions.csv"
EXL_FILE = DATA_DIR / "transactions_excel.xlsx"


def reader_csv_file(path_csv_file: str) -> List[Dict[str, Any]]:
    """Функция для считывания финансовых операций из CSV. Принимает путь к файлу CSV, в качестве аргумент,
    возвращает список словарей с транзакциями."""
    try:
        df_csv = pd.read_csv(path_csv_file, sep=";")
        transactions_csv_list = df_csv.to_dict(orient="records")

    except FileNotFoundError:
        raise FileNotFoundError(f"Ошибка: Файл не найден по пути {path_csv_file}")

    except ValueError as e:
        raise ValueError(f"Ошибка при чтении файла CSV: {e}")

    return transactions_csv_list


def reader_excel_file(path_excel_file: str) -> List[Dict[str, Any]]:
    """
     Функция для считывания финансовых операций из Excel. Принимает путь к файлу Excel, в качестве аргумента,
    и выдает список словарей с транзакциями.
    """
    try:
        df_exl = pd.read_excel(path_excel_file)
        transactions_exl_list = df_exl.to_dict(orient="records")
    except FileNotFoundError:
        raise FileNotFoundError(f"Ошибка: Файл не найден по пути {path_excel_file}")

    except ValueError as e:
        raise ValueError(f"Ошибка при чтении файла Excel: {e}")

    return transactions_exl_list
