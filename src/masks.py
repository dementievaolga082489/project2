import logging
import os

# Получаем путь к корневой директории проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(project_root, "logs", "masks.log")

# Создаем директорию, если она не существует
log_dir = os.path.dirname(log_path)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Принимает на вход номер карты и возвращает ее маску XXXX XX** **** XXXX."""

    # Проверяем, что передана строка
    if not isinstance(card_number, str):
        logger.error("Номер карты должен быть строкой")
        raise ValueError("Номер карты должен быть строкой")

    clean_card_number = card_number.replace(" ", "")

    if len(clean_card_number) != 16:
        logger.error("Номер карты должен содержать 16 цифр")
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Проверяем, что все символы - цифры
    if not clean_card_number.isdigit():
        logger.error("Номер карты должен содержать только цифры")
        raise ValueError("Номер карты должен содержать только цифры")

    mask = f"{clean_card_number[0:4]} {clean_card_number[4:6]}** **** {clean_card_number[-4:]}"
    logger.info(f"Номер карты отформатирован: {mask}")
    return mask


def get_mask_account(account_number: str) -> str:
    """Принимает на вход номер счета и возвращает его маску **XXXX."""

    if not account_number:
        logger.error("Номер счета не может быть пустым")
        raise ValueError("Номер счета не может быть пустым")

    if len(account_number) < 4:
        logger.error("Номер счета должен содержать минимум 4 символа")
        raise ValueError("Номер счета должен содержать минимум 4 символа")

    # Берем последние 4 символа
    last_four = account_number[-4:]
    logger.info(f"Счёт отформатирован: **{last_four}")

    return f"**{last_four}"
