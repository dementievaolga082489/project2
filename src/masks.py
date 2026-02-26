def get_mask_card_number(card_number: str) -> str:
    """Принимает на вход номер карты и возвращает ее маску XXXX XX** **** XXXX."""

    # Проверяем, что передана строка
    if not isinstance(card_number, str):
        raise ValueError("Номер карты должен быть строкой")

    clean_card_number = card_number.replace(" ", "")

    if len(clean_card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Проверяем, что все символы - цифры
    if not clean_card_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    mask = f"{clean_card_number[0:4]} {clean_card_number[4:6]}** **** {clean_card_number[-4:]}"
    return mask


def get_mask_account(account_number: str) -> str:
    """Принимает на вход номер счета и возвращает его маску **XXXX."""

    if not account_number:
        raise ValueError("Номер счета не может быть пустым")

    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 символа")

    # Берем последние 4 символа
    last_four = account_number[-4:]

    return f"**{last_four}"
