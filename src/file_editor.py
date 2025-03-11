import os.path
from abc import ABC, abstractmethod
import json
from fileinput import lineno
from pathlib import Path
from src.vacancy import Vacancy
from src.utils import get_currency_rates
import logging
import pandas as pd
import csv

ROOT_DIR = Path(__file__).resolve().parent.parent


file_editor_logger = logging.getLogger('file_editor')
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d')
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, 'logs', 'file_editor.log'), 'w')
file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d')
file_handler.setFormatter(file_formatter)
file_editor_logger.addHandler(file_handler)
file_editor_logger.addHandler(console_handler)
file_editor_logger.setLevel(logging.DEBUG)

class FileEditor(ABC):
    @abstractmethod
    def read_file(self, params):
        pass

    @abstractmethod
    def save_to_file(self, vacancies):
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass


class JSONEditor(FileEditor):
    def __init__(self, filename = f'{ROOT_DIR}\\data\\data.csv'):
        self.__filename = filename+'.json' if filename != 'data.json' and filename[-5:] != '.json' else filename


    def read_file(self, params = None):
        vacancies = []
        data = json.load(open(self.__filename, encoding='utf-8'))

        if params is not None:
            for vacancy in data:
                currency_multiplier = 1

                #file_editor_logger.debug(vacancy['salary'])

                salary: bool = (params.get('salary') is not None and
                    (vacancy['salary'] == 'Зарплата не указана' or (vacancy['salary']['from'] * currency_multiplier
                    <= params['salary'] <= vacancy['salary']['to'] * currency_multiplier)))
                keyword: bool = (params.get('keyword') is not None and (params['keyword'] in vacancy['name']))

                if (params.get('salary') is not None and
                        vacancy.get('salary') != 'Зарплата не указана' and
                        vacancy.get('salary').get('currency') != 'RUR'):
                    try:
                        currency_multiplier = get_currency_rates(vacancy['salary']['currency'])
                    except TypeError:
                        currency_multiplier = 1

                if salary or keyword:
                    vacancies.append(vacancy)
        else:
            for vacancy in data:
                vacancies.append(vacancy)
        return vacancies


    def save_to_file(self, vacancies):
        try:
            json_data = json.load(open(self.__filename, encoding='utf-8'))
            vacancies_id = []
            for vacancy in json_data:
                file_editor_logger.debug(vacancy)
                vacancies_id.append(vacancy['id'])

            for vacancy in vacancies:
                if vacancy['id'] in vacancies_id:
                    vacancies.remove(vacancy)
            json_data.append(vacancies)
            with open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            with open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)
        except json.JSONDecodeError:
            with open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)
        f.close()


    def add_vacancy(self, vacancy):
        try:
            json_data = json.load(open(self.__filename, encoding='utf-8'))
        except FileNotFoundError:
            raise FileNotFoundError('Файл не найден')
        except json.JSONDecodeError:
            with open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8') as f:
                f.write(json.dumps(vacancy, ensure_ascii=False, indent=4))

        vacancies_id = []

        for data in json_data:
            vacancies_id.append(data['id'])
        if vacancy['id'] not in vacancies_id:
            with open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8') as f:
                json_data.append(vacancy)
                f.write(json.dumps(json_data, ensure_ascii=False, indent=4))
            f.close()


    def delete_vacancy(self):
        open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8').close()


class ExcelEditor(FileEditor):
    def __init__(self, filename = 'vacancies.xlsx'):
        self.__filename = filename+'.xlsx' if filename != 'vacancies.xlsx' and filename[-5:] != '.xlsx' else filename

    def read_file(self, params=None):
        vacancies = []
        data = json.load(open(self.__filename, encoding='utf-8'))

        if params is not None:
            for vacancy in data:
                currency_multiplier = 1

                # file_editor_logger.debug(vacancy['salary'])

                salary: bool = (params.get('salary') is not None and
                                (vacancy['salary'] == 'Зарплата не указана' or (
                                            vacancy['salary']['from'] * currency_multiplier
                                            <= params['salary'] <= vacancy['salary']['to'] * currency_multiplier)))
                keyword: bool = (params.get('keyword') is not None and (params['keyword'] in vacancy['name']))

                if (params.get('salary') is not None and
                        vacancy.get('salary') != 'Зарплата не указана' and
                        vacancy.get('salary').get('currency') != 'RUR'):
                    try:
                        currency_multiplier = get_currency_rates(vacancy['salary']['currency'])
                    except TypeError:
                        currency_multiplier = 1

                if salary or keyword:
                    vacancies.append(vacancy)
        else:
            for vacancy in data:
                vacancies.append(vacancy)
        return vacancies

    def save_to_file(self, vacancies=None):
        try:
            with open(self.__filename, encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')
            csv_file.close()
            csv_data = list(filter(None, reader))
            vacancies_id = []
            for vacancy in csv_data:
                vacancies_id.append(vacancy['id'])

            for vacancy in vacancies:
                if vacancy['id'] in vacancies_id:
                    vacancies.remove(vacancy)
            csv_data.append(vacancies)
            with open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                for row in csv_data:
                    csv_writer.writerow(row)
            csv_file.close()
        except FileNotFoundError:
            with open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                for row in vacancies:
                    csv_writer.writerow(row)
            csv_file.close()
        except pd.errors:
            with open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                for row in vacancies:
                    csv_writer.writerow(row)
            csv_file.close()

    def add_vacancy(self, vacancy):
        try:
            json_data = json.load(open(self.__filename, encoding='utf-8'))
        except FileNotFoundError:
            raise FileNotFoundError('Файл не найден')
        except json.JSONDecodeError:
            with open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8') as f:
                f.write(json.dumps(vacancy, ensure_ascii=False, indent=4))

        vacancies_id = []

        for data in json_data:
            vacancies_id.append(data['id'])
        if vacancy['id'] not in vacancies_id:
            with open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8') as f:
                json_data.append(vacancy)
                f.write(json.dumps(json_data, ensure_ascii=False, indent=4))
            f.close()

    def delete_vacancy(self):
        open(os.path.join(ROOT_DIR, 'data', self.__filename), 'w', encoding='utf-8').close()


class CSVEditor(FileEditor):
    def __init__(self, filename = f'{ROOT_DIR}\\data\\data.csv'):
        self.__filename = filename+'.csv' if filename != 'data.csv' and filename[-4:] != '.csv' else filename

    def read_file(self, params = None):
        with open(self.__filename) as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row['Name'], row['Age'], row['Gender'])

    def save_to_file(self, vacancies):
        try:
            with open(self.__filename, encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
            vacancies_id = []
            for vacancy in reader:
                vacancies_id.append(vacancy['id'])
            for vacancy in vacancies:
                    if vacancy['id'] in vacancies_id:
                        vacancies.remove(vacancy)

            with open(self.__filename, 'a', encoding='utf-8', newline='') as file:
                fieldnames = ['id', 'name', 'salary', 'responsibility', 'requirement', 'url']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in vacancies:
                    writer.writerow(row)

        except Exception:
            with open(self.__filename, 'w', encoding='utf-8', newline='') as file:
                fieldnames = ['id', 'name', 'salary', 'responsibility', 'requirement', 'url']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in vacancies:
                    writer.writerow(row)



    def add_vacancy(self, vacancy):
        pass

    def delete_vacancy(self):
        pass
