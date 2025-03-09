import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(".env")

CURRENCY_RATE_API_KEY = os.getenv("CURRENCY_RATE_API_KEY")

ROOT_DIR = Path(__file__).resolve().parent.parent

utils_logger = logging.getLogger("utils")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "utils.log"), "w")
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.addHandler(console_handler)
utils_logger.setLevel(logging.DEBUG)

def get_currency_rates(currency: str) -> list:
    """
    :param currency: список валют
    Функция обращается к внешнему API и возвращает курсы валют из списка
    """

    currency += "RUB"
    utils_logger.debug(currency)
    url = f"https://currate.ru/api/?get=rates&pairs={currency}&key={CURRENCY_RATE_API_KEY}"

    payload = {}
    headers = {"apikey": CURRENCY_RATE_API_KEY}

    response = requests.request("GET", url, headers=headers, data=payload)
    status_code = response.status_code
    if status_code == 400:
        utils_logger.warning("Bad Request")
        print("Bad Request")
    if status_code == 401:
        utils_logger.warning("Unauthorized")
        print("Unauthorized")
    if status_code == 404:
        utils_logger.warning("Not Found")
        print("Not Found")
    if status_code == 429:
        utils_logger.warning("Too many requests")
        print("Too many requests")
    if status_code == 500:
        utils_logger.warning("Server Error")
        print("Server Error")

    result = response.json().get("data")
    result = float(result[currency])

    utils_logger.info("Функция выполнена успешно")
    return int(result)