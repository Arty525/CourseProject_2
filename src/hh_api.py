import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path

import requests

from src.vacancy import Vacancy

ROOT_DIR = Path(__file__).resolve().parent.parent

hh_api_logger = logging.getLogger("hh_api")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d"
)
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "hh_api.log"), "w")
file_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d"
)
file_handler.setFormatter(file_formatter)
hh_api_logger.addHandler(file_handler)
hh_api_logger.addHandler(console_handler)
hh_api_logger.setLevel(logging.DEBUG)


class HeadHunterAPI(ABC):
    """
    Базовый класс для работы с API HeadHunter
    """

    @abstractmethod
    def _connect_api(self):
        """
        Функция проверяет подключение к базовому url hh.ru
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str):
        """
        Функция получает на вход ключевые слова в виде строки,
        выполняет запрос на внешний API и возвращает список вакансий в которых присутствуют указанные слова.
        """
        pass


class HH(HeadHunterAPI):
    """
    Класс для работы с API hh.ru
    """

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__base_url = "https://api.hh.ru/"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []

    def _connect_api(self) -> bool:
        try:
            requests.get(self.__base_url, headers=self.__headers)
            print("Соединение установлено")
            return True
        except requests.exceptions.ConnectionError as conncection_err:
            hh_api_logger.error("Connection Error")
            raise conncection_err
        except requests.exceptions.Timeout as timeout:
            hh_api_logger.error("Timeout")
            raise timeout
        except requests.exceptions.HTTPError as http_err:
            hh_api_logger.error("HTTP error occurred")
            raise http_err
        except requests.exceptions.TooManyRedirects as too_many_redirects:
            hh_api_logger.error("Too Many Redirects")
            raise too_many_redirects

    def cast_vacancies(self) -> list:
        """
        Функция создает список из объектов класса Vacancy и возвращает его
        """
        vacancies_list = []
        for vacancy in self.__vacancies:
            # ("id", "name", "responsibility", "salary", "requirement", "url")
            vacancies_list.append(
                Vacancy(
                    vacancy["id"],
                    vacancy["name"],
                    vacancy["snippet"]["responsibility"],
                    vacancy["salary"],
                    vacancy["snippet"]["requirement"],
                    vacancy["url"],
                )
            )
        return vacancies_list

    def get_vacancies(self, keyword: str) -> list:
        """
        Функция получает список вакансий с hh.ru и возвращает список объектов класса Vacancy
        """
        try:
            self._connect_api()
        except requests.exceptions.ConnectionError:
            hh_api_logger.error("Connection Error")
            return []
        self.__params["text"] = keyword
        while self.__params.get("page") != 20:
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            vacancies = response.json()["items"]
            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1
        return self.cast_vacancies()
