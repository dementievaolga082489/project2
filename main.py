from src.bank_operations import process_bank_search
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.transaction_reader import CSV_FILE, EXL_FILE, reader_csv_file, reader_excel_file
from src.utils import read_json_file
from src.widget import get_date, mask_account_card


def main() -> None:
    """ Функция, которая отвечает за основную логику проекта с пользователем и связывает функциональности между собой."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n")
    while True:

        print(
            "Выберите необходимый пункт меню:\n"
            "1. Получить информацию о транзакциях из JSON-файла\n"
            "2. Получить информацию о транзакциях из CSV-файла\n"
            "3. Получить информацию о транзакциях из XLSX-файла\n"
        )
        user_choice = input("\nВаш выбор: ")
        if user_choice == "1":
            print("Для обработки выбран JSON-файл.")
            transactions = read_json_file("data/operations.json")
            break
        elif user_choice == "2":
            print("Для обработки выбран CSV-файл.")
            transactions = reader_csv_file(CSV_FILE)
            break
        elif user_choice == "3":
            print("Для обработки выбран EXCEL-файл.")
            transactions = reader_excel_file(EXL_FILE)
            break
        else:
            print("\nНеверный выбор. Выберите 1, 2 или 3")

    # Фильтрация по статусу
    while True:
        print(
            "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING."
        )
        status = ["EXECUTED", "CANCELED", "PENDING"]
        user_status = (input("\nВаш выбор: ")).strip().upper()
        if user_status in status:
            state = user_status
            print(f"Операции отфильтрованы по статусу {state}")
            operations_by_state = filter_by_state(transactions, state)
            break
        else:
            print(f"Статус операции {user_status} недоступен.")
    # Сортировка по дате
    while True:
        sort_by_data_choice = (input("\nОтсортировать операции по дате? Да/Нет\n")).strip().lower()
        if sort_by_data_choice in ["да", "нет"]:
            if sort_by_data_choice == "да":
                while True:
                    order_choice = (input("\nОтсортировать по возрастанию или по убыванию?\n")).strip().lower()
                    if order_choice == "по возрастанию":
                        order_filter = False
                        operations_sort_by_data = sort_by_date(operations_by_state, order_filter)
                        break
                    elif order_choice == "по убыванию":
                        order_filter = True
                        operations_sort_by_data = sort_by_date(operations_by_state, order_filter)
                        break
                    else:
                        print(f'Ввод "{order_choice}" некорректен. Пожалуйста, попробуйте снова.')
                break
            else:
                operations_sort_by_data = operations_by_state
                break

        else:
            print(f"Ввод {sort_by_data_choice} некорректен . Наберите Да или Нет")

    # Фильтрация по рублевым транзакциям
    while True:
        currency_filter = (input("\nВыводить только рублёвые транзакции? Да/Нет\n")).strip().lower()
        if currency_filter == "нет":
            transactions_lst = operations_sort_by_data
            break
        elif currency_filter == "да":
            currency_cod_ = "RUB"
            if user_choice == "1":  # JSON
                transactions_lst = list(filter_by_currency(operations_sort_by_data, currency_cod_))
                break
            elif user_choice == "2":  # CSV
                transactions_lst = list(filter_by_currency(operations_sort_by_data, currency_cod_))
                break
            elif user_choice == "3":  # XLSX
                transactions_lst = list(filter_by_currency(operations_sort_by_data, currency_cod_))
                break
        else:
            print(f'Ввод "{currency_filter}" некорректен. Наберите Да или Нет.')

    # Фильтрация по слову в описании
    while True:
        word_filter = (
            input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()
        )
        if word_filter == "да":
            search_word = input("Введите слово для фильтрации транзакций по описанию: ").strip().lower()
            filtered_transactions = process_bank_search(transactions_lst, search_word)
            break
        elif word_filter == "нет":
            filtered_transactions = transactions_lst
            break
        else:
            print(f'Ввод "{word_filter}" некорректен. Наберите Да или Нет.')

    print("\nРаспечатываю итоговый список транзакций...")
    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}\n")
        for transaction in filtered_transactions:
            data_str = get_date(transaction.get("date", ""))
            description = transaction.get("description", "")

            from_str = mask_account_card(transaction.get("from", ""))
            to_str = mask_account_card(transaction.get("to", ""))
            # Формируем строку перевода
            transfer_str = ""
            if from_str and to_str:
                transfer_str = f"{from_str} -> {to_str}"
            elif to_str:
                transfer_str = to_str

            oper_amount = transaction.get("operationAmount", {}).get("amount")
            amount_name_ = transaction.get("operationAmount", {}).get("currency", {}).get("name")
            amount_key = oper_amount if user_choice == "1" else transaction.get("amount")
            currency_key = amount_name_ if user_choice == "1" else transaction.get("currency_code")
            # Выводим транзакцию
            print(f"{data_str} {description}")
            print(f"{transfer_str}")
            print(f"Сумма: {amount_key} {currency_key} ")
            print()  # Пустая строка м


if __name__ == "__main__":
    main()
