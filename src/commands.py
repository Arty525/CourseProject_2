import logging
import os
import random
from pathlib import Path

from src.file_editor import CSVEditor, ExcelEditor, JSONEditor
from src.hh_api import HH
from src.vacancy import Vacancy, cast_vacancies_from_dict

ROOT_DIR = Path(__file__).resolve().parent.parent

commands_logger = logging.getLogger("commands")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d"
)
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "commands.log"), "w")
file_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d"
)
file_handler.setFormatter(file_formatter)
commands_logger.addHandler(file_handler)
commands_logger.addHandler(console_handler)
commands_logger.setLevel(logging.DEBUG)


def get_top() -> list:
    """
    Функция возвращает топ вакансий
    """
    print("Вы выбрали получение ТОП-вакансий по зарплате")
    number = input("Введите количество вакансий в выборке: ")
    while not number.isdigit():
        print("Вы ввели недопустимое значение. Введите число.\n")
        number = input("Введите количество вакансий в выборке: ")
    number = int(number)
    top_vacancies = []
    print(f"Выполняется выборка из {number} вакансий")
    try:
        json_editor = JSONEditor()
        vacancies = json_editor.read_file()
        for vacancy in vacancies:
            if vacancy.salary != "Зарплата не указана":
                top_vacancies.append(vacancy)
        top_vacancies = sorted(
            top_vacancies,
            key=lambda v: v.salary.get("to"),
            reverse=True,
        )
        return top_vacancies[:number]
    except FileNotFoundError:
        try:
            csv_editor = CSVEditor()
            vacancies = csv_editor.read_file()
            for vacancy in vacancies:
                if vacancy.salary != "Зарплата не указана":
                    top_vacancies.append(vacancy)
            top_vacancies = sorted(
                top_vacancies,
                key=lambda v: v.salary.get("to"),
                reverse=True,
            )
            return top_vacancies[:number]
        except FileNotFoundError:
            try:
                excel_editor = ExcelEditor()
                vacancies = excel_editor.read_file()
                for vacancy in vacancies:
                    if vacancy.salary != "Зарплата не указана":
                        top_vacancies.append(vacancy)
                top_vacancies = sorted(
                    top_vacancies,
                    key=lambda v: v.salary.get("to"),
                    reverse=True,
                )
                return top_vacancies[:number]
            except FileNotFoundError:
                raise FileNotFoundError("Файл не найден")


def get_vacancies_from_hh():
    """
    Функция принимает команды от пользователя и записывает вакансии с hh.ru в файлы
    """
    print("Вы выбрали получение данных с hh.ru")
    keyword = input("Введите ключевые слова для поиска: ")
    hh_api = HH()
    data = hh_api.get_vacancies(keyword)
    print("Данные успешно получены")
    if data is None or data == []:
        print("Не удалось получить вакансии по вашему запросу")
    else:
        # JSON
        try:
            json_editor = JSONEditor()
            json_editor.save_to_file(data)
            print("Данные сохранены в JSON-файл")
        except Exception as e:
            print(f"Не удалось сохранить данные в JSON-файл. Возникла ошибка: {e}")
            raise e
        finally:
            # CSV
            try:
                csv_editor = CSVEditor()
                csv_editor.save_to_file(data)
                print("Данные сохранены в CSV-файл")
            except Exception as e:
                print(f"Не удалось сохранить данные в CSV-файл. Возникла ошибка: {e}")
                raise e
            finally:
                # EXCEL
                try:
                    data = cast_vacancies_from_dict(data)
                    excel_editor = ExcelEditor()
                    excel_editor.save_to_file(data)
                    print("Данные сохранены в EXCEL-файл")
                except Exception as e:
                    print(
                        f"Не удалось сохранить данные в EXCEL-файл. Возникла ошибка: {e}"
                    )
                    raise e
        print("Данные успешно сохранены в папку data")


def search_vacancies() -> list:
    """
    Функция принимает от пользователя параметры запроса, выполняет поиск по локальным файлам и возвращает список
    вакансий.
    """
    print("Вы выбрали поиск по вакансиям")
    file_type = input("Введите тип файла для поиска (json, csv, excel): ").lower()
    while file_type not in ["json", "csv", "excel"]:
        print("Неверный тип файла. Повторите ввод.\n")
        file_type = input("Введите тип файла для поиска (json, csv, excel): ").lower()
    print("Введите параметры для поиска или оставьте поле пустым")
    salary = input("Введите зарплату в рублях: ")
    while not salary.isdigit() and salary != "":
        print("Неверное значение, введите число или оставьте поле пустым")
        salary = input("Введите зарплату в рублях: ")
    if salary.isdigit():
        salary = int(salary)
    keyword = input("Введите ключевое слово: ").lower()
    params = {"keyword": keyword, "salary": salary}
    vacancies = []
    if "csv" in file_type:
        csv_reader = CSVEditor()
        vacancies = csv_reader.read_file(params)
        if vacancies is None or vacancies == []:
            print("Не удалось найти вакансии по вашему запросу")
            return []
    elif "json" in file_type:
        json_reader = JSONEditor()
        vacancies = json_reader.read_file(params)
        if vacancies is None or vacancies == []:
            print("Не удалось найти вакансии по вашему запросу")
            return []
    elif "excel" in file_type:
        excel_reader = ExcelEditor()
        vacancies = excel_reader.read_file(params)
        if vacancies is None or vacancies == []:
            print("Не удалось найти вакансии по вашему запросу")
            return []
    return vacancies


def add_vacancy_to_file():
    """
    Функция принимает от пользователя данные о вакансии и записывает ее в файлы
    """
    print("Вы выбрали добавление вакансии в файл")
    print("Введите данные или оставьте поле пустым")
    name = input("Введите название вакансии: ")
    responsibility = input("Введите описание вакансии: ")
    requirement = input("Введите требуемые навыки: ")
    salary_from = input("Введите начальную зарплату в рублях: ")
    while not salary_from.isdigit() and salary_from != "":
        print("Неверное значение, введите число или оставьте поле пустым")
        salary_from = input("Введите начальную зарплату в рублях: ")
    if salary_from.isdigit():
        salary_from = int(salary_from)
    salary_to = input("Введите максимальную зарплату в рублях: ")
    while not salary_to.isdigit() and salary_to != "":
        print("Неверное значение, введите число или оставьте поле пустым")
        salary_to = input("Введите максимальную зарплату в рублях: ")
    if salary_to.isdigit():
        salary_to = int(salary_to)
    salary_currency = "RUR"
    id = str(random.randint(100000000, 999999999))
    url = input("Введите ссылку на вакансию: ")

    if salary_from != "" and salary_to != "":
        salary = {
            "from": int(salary_from),
            "to": int(salary_to),
            "currency": salary_currency,
        }
    elif salary_from == "" and salary_to != "":
        salary = {"from": 0, "to": int(salary_to), "currency": salary_currency}
    elif salary_from != "" and salary_to == "":
        salary = {
            "from": int(salary_from),
            "to": int(salary_from),
            "currency": salary_currency,
        }
    else:
        salary = "Зарплата не указана"
    vacancy = Vacancy(id, name, responsibility, salary, requirement, url)
    file_type = input("Выберите тип файла (json, csv, excel): ").lower()
    while file_type not in ["json", "csv", "excel"]:
        print("Неверный тип файла, повторите ввод.")
        file_type = input("Выберите тип файла (json, csv, excel): ").lower()
    if "csv" in file_type:
        csv_editor = CSVEditor()
        try:
            csv_editor.add_vacancy(vacancy)
            print("Вакансия успешно добавлена")
        except Exception as e:
            raise e
    elif "json" in file_type:
        json_editor = JSONEditor()
        try:
            json_editor.add_vacancy(vacancy)
            print("Вакансия успешно добавлена")
        except Exception as e:
            raise e
    elif "excel" in file_type:
        excel_editor = ExcelEditor()
        try:
            excel_editor.add_vacancy(vacancy)
            print("Вакансия успешно добавлена")
        except Exception as e:
            raise e
    else:
        json_editor = JSONEditor()
        try:
            json_editor.add_vacancy(vacancy)
            print("Вакансия успешно добавлена")
        except Exception as e:
            raise e
