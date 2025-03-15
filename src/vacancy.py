import logging
import os
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent

vacancy_logger = logging.getLogger("vacancy")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d"
)
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "vacancy.log"), "w")
file_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d"
)
file_handler.setFormatter(file_formatter)
vacancy_logger.addHandler(file_handler)
vacancy_logger.addHandler(console_handler)
vacancy_logger.setLevel(logging.DEBUG)


class Vacancy:
    """
    Класс для работы с вакансиями
    """

    __slots__ = ("id", "name", "responsibility", "salary", "requirement", "url")

    def __init__(
        self,
        id: str,
        name: str,
        responsibility: str,
        salary: Any,
        requirement: str,
        url: str,
    ):
        self.id = id
        self.name = name.lower()
        self.responsibility = responsibility
        self.salary = self.__validate(salary)
        self.requirement = requirement
        self.url = url

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Vacancy):
            if type(self.salary) is not str and type(other.salary) is not str:
                return self.salary["to"] < other.salary["to"]
            else:
                return False

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Vacancy):
            if type(self.salary) is not str and type(other.salary) is not str:
                return self.salary["to"] > other.salary["to"]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Vacancy):
            if type(self.salary) is not str and type(other.salary) is not str:
                return self.salary["to"] == other.salary["to"]
            else:
                return False

    def __str__(self):
        salary = ""
        if self.salary == "Зарплата не указана":
            salary = self.salary
        else:
            if self.salary.get("from") is not None:
                salary += f'от {self.salary["from"]} '
            if self.salary.get("to") is not None:
                salary += f'до {self.salary["to"]}'
        return (
            f"{self.name}\nЗарплата: {salary}\nОписание вакансии: {self.responsibility}\n"
            f"Требования: {self.requirement}\nURL: {self.url}\n{'-'*50}"
        )

    def __validate(self, salary: Any) -> Any:
        """
        Функция принимает на вход значение поля "salary" и возвращает корректное значение
        """
        if salary == "":
            salary = "Зарплата не указана"
        if salary is not None and salary != "Зарплата не указана":
            if type(salary) is str:
                salary = eval(salary)
            if salary["from"] is None or int(salary["from"]) <= 0:
                salary["from"] = 0
            if salary["to"] is None or int(salary["to"]) <= 0:
                salary["to"] = 0
            return salary
        return "Зарплата не указана"

    def get_as_dict(self) -> dict:
        """
        Функция возвращает вакансию в виде словаря
        """
        return {
            "id": self.id,
            "name": self.name,
            "salary": self.salary,
            "responsibility": self.responsibility,
            "requirement": self.requirement,
            "url": self.url,
        }


def cast_vacancies_from_dict(vacancies: list) -> list:
    """
    Функция принимает список вакансий в виде словарей и возвращает список вакансий в виде объектов класса Vacancy
    """
    for i in range(len(vacancies)):
        if vacancies[i] is str:
            vacancies[i] = eval(vacancies[i])
        vacancies[i] = Vacancy(
            vacancies[i]["id"],
            vacancies[i]["name"],
            vacancies[i]["responsibility"],
            vacancies[i]["salary"],
            vacancies[i]["requirement"],
            vacancies[i]["url"],
        )
    return vacancies
