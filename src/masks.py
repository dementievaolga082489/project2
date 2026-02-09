def get_mask_card_number(card_number: int) -> str:
    """Принимает на вход номер карты и возвращает ее маску XXXX XX** **** XXXX."""

    clean_card_number = str(card_number)

    if len(clean_card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    mask = f"{clean_card_number[0:4]} {clean_card_number[5:7]}** **** {clean_card_number[-4:]}"
    return mask


def get_mask_account(card_number: int) -> str:
    """Принимает на вход номер счета и возвращает его маску **XXXX."""

    clean_card_number = str(card_number)
    mask = f"**{clean_card_number[-4:]}"

    return mask
