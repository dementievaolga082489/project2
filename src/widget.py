from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""

    # Проверка, что это строка
    if not isinstance(info, str):
        return info

    # Проверка на пустую строку
    if info == "":
        return ""

    # Разделяем строку на слова
    new_info = info.split()

    # Если после удаления пробелов строка пустая
    if not new_info:
        return info

    # Если последнее слово состоит из 16 цифр
    if new_info[-1].isdigit() and len(new_info[-1]) == 16:
        card_number = new_info[-1]
        mask_number = get_mask_card_number(card_number)
        return f"{' '.join(new_info[:-1])} {mask_number}"

    # Если начинается со слова "счет" и последнее слово состоит из 20 цифр
    elif new_info[0] == "Счет" and new_info[-1].isdigit() and len(new_info[-1]) == 20:
        account_number = new_info[-1]
        mask_number = get_mask_account(account_number)
        return f"{' '.join(new_info[:-1])} {mask_number}"
    return info


def get_date(data: str) -> str:
    """которая принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407"
     и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ"
     (
    "11.03.2024"
    )."""
    if data is None:
        return "Ошибка: пустая строка или некорректный тип данных"

    if not isinstance(data, str):
        return "Ошибка: пустая строка или некорректный тип данных"

    if not data or not data.strip():
        return "Ошибка: пустая строка или некорректный тип данных"

    data = data.strip()

    # Проверяем, что строка содержит корректный разделитель даты и времени
    if "T" in data:
        # Разделяем по первому 'T'
        parts = data.split("T", 1)  # Разделяем только по первому вхождению

        # Проверяем, что после T есть хотя бы один символ и это не просто пробел
        if len(parts) != 2 or not parts[1] or not parts[1].strip():
            return "Ошибка: неверный формат даты (отсутствует время)"

        date_part = parts[0]
    else:
        date_part = data

    # Разделяем дату по '-'
    date_components = date_part.split("-")

    # Проверяем, что получили 3 компонента (год, месяц, день)
    if len(date_components) != 3:
        return "Ошибка: неверный формат даты"

    year, month, day = date_components

    # Проверяем, что компоненты не пустые
    if not (year and month and day):
        return "Ошибка: неверный формат даты"

    # Проверяем, что компоненты являются числами
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return "Ошибка: компоненты даты должны быть числами"

    # Преобразуем в числа для валидации
    year_int = int(year)
    month_int = int(month)
    day_int = int(day)

    # Проверяем корректность месяца
    if not (1 <= month_int <= 12):

        return "Ошибка: месяц должен быть от 1 до 12"

    # Проверяем корректность дня
    if not (1 <= day_int <= 31):
        return "Ошибка: день должен быть от 1 до 31"

    # Проверка количества дней в месяце
    days_in_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    # Проверка на високосный год для февраля
    if month_int == 2:
        # Проверка високосности
        is_leap = (year_int % 4 == 0 and year_int % 100 != 0) or (year_int % 400 == 0)
        max_days = 29 if is_leap else 28

        if day_int > max_days:
            return f"Ошибка: в феврале {year} года только {max_days} дней"
    else:
        # Для остальных месяцев
        if day_int > days_in_month[month_int]:
            return f"Ошибка: в месяце {month_int} только {days_in_month[month_int]} дней"

    return f"{day}.{month}.{year}"
