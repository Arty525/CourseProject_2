import csv
import json
import logging
import os.path
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import pandas as pd

from src.utils import get_currency_rates
from src.vacancy import Vacancy, cast_vacancies_from_dict

ROOT_DIR = Path(__file__).resolve().parent.parent


file_editor_logger = logging.getLogger("file_editor")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d"
)
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(
    os.path.join(ROOT_DIR, "logs", "file_editor.log"), "w"
)
file_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d"
)
file_handler.setFormatter(file_formatter)
file_editor_logger.addHandler(file_handler)
file_editor_logger.addHandler(console_handler)
file_editor_logger.setLevel(logging.DEBUG)


class FileEditor(ABC):
    """
    Базовый класс для работы с файлами
    """

    @abstractmethod
    def read_file(self, params: Any):
        """
        Функция принимает на вход параметры для поиска и возвращает список вакансий, подходящих
        под указанные параметры. Поиск выполняется по ключевому слову и зарплате.
        """
        pass

    @abstractmethod
    def save_to_file(self, vacancies: list):
        """
        Функция принимает список вакансий и сохраняет их в файл
        """
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        """
        Функция принимает вакансию и добавляет ее в файл.
        """
        pass

    @abstractmethod
    def delete_vacancy(self):
        """
        Функция удаляет список вакансий из локального файла
        """
        pass


class JSONEditor(FileEditor):
    """
    Класс для работы с JSON-файлами
    """

    def __init__(self, filename=os.path.join(ROOT_DIR, "data", "json_data.json")):
        self.__filename = (
            filename + ".json"
            if filename != "json_data.json" and filename[-5:] != ".json"
            else filename
        )

    def read_file(self, params: Any = None) -> list:
        vacancies = []
        try:
            data = json.load(open(self.__filename, encoding="utf-8"))
            print("Выполняется поиск по JSON-файлу")
            if params is not None:
                for vacancy in data:
                    currency_multiplier = 1
                    if (
                        params.get("salary") != ""
                        and vacancy.get("salary") != "Зарплата не указана"
                        and vacancy.get("salary").get("currency") != "RUR"
                    ):
                        try:
                            currency_multiplier = get_currency_rates(
                                vacancy["salary"]["currency"]
                            )
                        except TypeError:
                            currency_multiplier = 1

                    is_salary: bool = True
                    if params["salary"] == "":
                        is_salary = True
                    else:
                        is_salary: bool = vacancy[
                            "salary"
                        ] == "Зарплата не указана" or (
                            vacancy["salary"]["from"] * currency_multiplier
                            <= params["salary"]
                            <= vacancy["salary"]["to"] * currency_multiplier
                        )
                    is_keyword: bool = params.get("keyword") == "" or (
                        params["keyword"].lower() in vacancy["name"].lower()
                    )

                    if is_salary and is_keyword:
                        vacancies.append(vacancy)

            else:
                for vacancy in data:
                    vacancies.append(vacancy)
            return cast_vacancies_from_dict(vacancies)
        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден")

    def save_to_file(self, vacancies: list):
        try:
            vacancies_id = []
            with open(self.__filename, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for vacancy in json_data:
                    vacancies_id.append(vacancy["id"])

            for vacancy in vacancies:
                if vacancy.id not in vacancies_id:
                    json_data.append(vacancy.get_as_dict())
            with open(
                os.path.join(ROOT_DIR, "data", self.__filename), "w", encoding="utf-8"
            ) as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            with open(
                os.path.join(ROOT_DIR, "data", self.__filename), "w", encoding="utf-8"
            ) as f:
                vacancies_dict = []
                for vacancy in vacancies:
                    vacancies_dict.append(vacancy.get_as_dict())
                json.dump(vacancies_dict, f, ensure_ascii=False, indent=4)
        except json.JSONDecodeError:
            with open(
                os.path.join(ROOT_DIR, "data", self.__filename), "w", encoding="utf-8"
            ) as f:
                vacancies_dict = []
                for vacancy in vacancies:
                    vacancies_dict.append(vacancy.get_as_dict())
                json.dump(vacancies_dict, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy):
        json_data = []
        try:
            json_data = json.load(open(self.__filename, encoding="utf-8"))
        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден")
        except json.JSONDecodeError:
            with open(
                os.path.join(ROOT_DIR, "data", self.__filename), "w", encoding="utf-8"
            ) as f:
                f.write(json.dumps(vacancy.get_as_dict(), ensure_ascii=False, indent=4))

        vacancies_id = []

        for data in json_data:
            vacancies_id.append(data["id"])
        if vacancy.id not in vacancies_id:
            with open(
                os.path.join(ROOT_DIR, "data", self.__filename), "w", encoding="utf-8"
            ) as f:
                json_data.append(vacancy.get_as_dict())
                f.write(json.dumps(json_data, ensure_ascii=False, indent=4))
            f.close()

    def delete_vacancy(self):
        with open(
            os.path.join(ROOT_DIR, "data", self.__filename), "w", encoding="utf-8"
        ) as f:
            json.dump([], f, ensure_ascii=False, indent=4)


class ExcelEditor(FileEditor):
    """
    Класс для работы с Excel-файлами
    """

    def __init__(self, filename=os.path.join(ROOT_DIR, "data", "excel_data.xlsx")):
        self.__filename = (
            filename + ".xlsx"
            if filename != "excel_data.xlsx" and filename[-5:] != ".xlsx"
            else filename
        )

    def read_file(self, params: Any = None) -> list:
        try:
            excel_data = pd.read_excel(self.__filename)
            print("Выполняется поиск по EXCEL-файлу")
            data = excel_data.to_dict("records")
            vacancies = []
            if params is not None:
                for vacancy in data:
                    currency_multiplier = 1
                    if (
                        params.get("salary") != ""
                        and vacancy.get("salary") != "Зарплата не указана"
                    ):
                        if eval(str(vacancy.get("salary"))).get("currency") != "RUR":
                            try:
                                currency_multiplier = get_currency_rates(
                                    eval(vacancy["salary"])["currency"]
                                )
                            except TypeError:
                                currency_multiplier = 1

                    is_salary: bool = True
                    if params["salary"] == "":
                        is_salary = True
                    else:
                        is_salary: bool = vacancy[
                            "salary"
                        ] == "Зарплата не указана" or (
                            eval(str(vacancy["salary"]))["from"] * currency_multiplier
                            <= params["salary"]
                            <= eval(str(vacancy["salary"]))["to"] * currency_multiplier
                        )
                    is_keyword: bool = params.get("keyword") == "" or (
                        params["keyword"].lower() in vacancy["name"].lower()
                    )

                    if is_salary and is_keyword:
                        vacancies.append(vacancy)
            else:
                for vacancy in data:
                    vacancies.append(vacancy)
            return cast_vacancies_from_dict(vacancies)
        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден")

    def save_to_file(self, vacancies: list):
        try:
            excel_data = pd.read_excel(self.__filename)
            vacancies_id = excel_data["id"]
            vacancies_list = []
            for vacancy in vacancies:
                if vacancy.id not in vacancies_id:
                    vacancies_list.append(vacancy.get_as_dict())
            fieldnames = [
                "id",
                "name",
                "salary",
                "responsibility",
                "requirement",
                "url",
            ]
            dataframe = pd.DataFrame(data=vacancies_list, columns=fieldnames)
            dataframe.to_excel(self.__filename, index=False)
        except FileNotFoundError:
            fieldnames = [
                "id",
                "name",
                "salary",
                "responsibility",
                "requirement",
                "url",
            ]
            for i in range(len(vacancies)):
                vacancies[i] = vacancies[i].get_as_dict()
            dataframe = pd.DataFrame(data=vacancies, columns=fieldnames)
            dataframe.to_excel(self.__filename, index=False)
        except Exception as e:
            fieldnames = [
                "id",
                "name",
                "salary",
                "responsibility",
                "requirement",
                "url",
            ]
            for i in range(len(vacancies)):
                vacancies[i] = vacancies[i].get_as_dict()
            dataframe = pd.DataFrame(data=vacancies, columns=fieldnames)
            dataframe.to_excel(self.__filename, index=False)
            raise e

    def add_vacancy(self, vacancy: Vacancy):
        try:
            excel_data = pd.read_excel(self.__filename)
        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден")
        vacancies_id = excel_data["id"]
        data = excel_data.to_dict("records")
        if vacancy.id not in vacancies_id:
            data.append(vacancy.get_as_dict())
        fieldnames = ["id", "name", "salary", "responsibility", "requirement", "url"]
        dataframe = pd.DataFrame(data=data, columns=fieldnames)
        dataframe.to_excel(self.__filename, index=False)

    def delete_vacancy(self):
        fieldnames = ["id", "name", "salary", "responsibility", "requirement", "url"]
        dataframe = pd.DataFrame(data=[], columns=fieldnames)
        dataframe.to_excel(self.__filename, index=False)


class CSVEditor(FileEditor):
    """
    Класс для работы с CSV-файлами
    """

    def __init__(self, filename=os.path.join(ROOT_DIR, "data", "csv_data.csv")):
        self.__filename = (
            filename + ".csv"
            if filename != "csv_data.csv" and filename[-4:] != ".csv"
            else filename
        )

    def read_file(self, params: Any = None) -> list:
        try:
            vacancies = []
            with open(self.__filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                print("Выполняется поиск по CSV-файлу")
                data = list(filter(None, reader))
                if params is not None:
                    for row in data:
                        currency_multiplier = 1
                        if (
                            params.get("salary") != ""
                            and row.get("salary") != "Зарплата не указана"
                        ):
                            if eval(row.get("salary")).get("currency") != "RUR":
                                try:
                                    currency_multiplier = get_currency_rates(
                                        eval(row["salary"])["currency"]
                                    )
                                except TypeError:
                                    currency_multiplier = 1

                        is_salary: bool = True
                        if params["salary"] == "":
                            is_salary = True
                        else:
                            is_salary: bool = row[
                                "salary"
                            ] == "Зарплата не указана" or (
                                eval(row["salary"])["from"] * currency_multiplier
                                <= params["salary"]
                                <= eval(row["salary"])["to"] * currency_multiplier
                            )
                        is_keyword: bool = params.get("keyword") == "" or (
                            params["keyword"].lower() in row["name"].lower()
                        )

                        if is_salary and is_keyword:
                            vacancies.append(row)
                else:
                    return data
            return cast_vacancies_from_dict(vacancies)
        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден")

    def save_to_file(self, vacancies: list):
        for i in range(len(vacancies)):
            vacancies[i] = vacancies[i].get_as_dict()
        try:
            with open(self.__filename, encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
            vacancies_id = []
            for vacancy in reader:
                vacancies_id.append(vacancy["id"])
            for vacancy in vacancies:
                if vacancy["id"] in vacancies_id:
                    vacancies.remove(vacancy)

            with open(self.__filename, "a", encoding="utf-8", newline="") as file:
                fieldnames = [
                    "id",
                    "name",
                    "salary",
                    "responsibility",
                    "requirement",
                    "url",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in vacancies:
                    writer.writerow(row)

        except Exception:
            with open(self.__filename, "w", encoding="utf-8", newline="") as file:
                fieldnames = [
                    "id",
                    "name",
                    "salary",
                    "responsibility",
                    "requirement",
                    "url",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in vacancies:
                    writer.writerow(row)

    def add_vacancy(self, vacancy: Vacancy):
        try:
            vacancies_id = []
            with open(self.__filename, "r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    vacancies_id.append(row["id"])
            if vacancy.id not in vacancies_id:
                with open(self.__filename, "a", encoding="utf-8", newline="") as file:
                    fieldnames = [
                        "id",
                        "name",
                        "salary",
                        "responsibility",
                        "requirement",
                        "url",
                    ]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writerow(vacancy.get_as_dict())
        except Exception:
            with open(self.__filename, "w", encoding="utf-8", newline="") as file:
                fieldnames = [
                    "id",
                    "name",
                    "salary",
                    "responsibility",
                    "requirement",
                    "url",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(vacancy.get_as_dict())
    def delete_vacancy(self):
        with open(self.__filename, "w", encoding="utf-8", newline="") as file:
            fieldnames = [
                "id",
                "name",
                "salary",
                "responsibility",
                "requirement",
                "url",
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
