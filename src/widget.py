from src.masks import get_mask_account, get_mask_card_number

def mask_account_card(info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""


#Разделяем строку на слова
    new_info = info.split()

#Если последнее слово состоит из 16 цифр
    if new_info[-1].isdigit() and len(new_info[-1]) == 16:
        card_number = new_info[-1]
        mask_number = get_mask_card_number(card_number)
        return f"{' '.join(new_info[:-1])} {mask_number}"

#Если начинается со слова "счет" и последнее слово состоит из 20 цифр
    elif new_info[0] == "Счет" and new_info[-1].isdigit() and len(new_info[-1]) == 20:
        account_number = new_info[-1]
        mask_number = get_mask_account(account_number)
        return f"{' '.join(new_info[:-1])} {mask_number}"


def get_date(data:str) -> str:

    """которая принимает на вход строку с датой в формате
"2024-03-11T02:26:18.671407"
 и возвращает строку с датой в формате
"ДД.ММ.ГГГГ"
 (
"11.03.2024"
)."""
    new_data = data.split("T")[0]
    year, month, day = new_data.split("-")
    return f"{day}.{month}.{year}"

