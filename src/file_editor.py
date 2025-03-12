import os.path
from abc import ABC, abstractmethod
import json
from fileinput import lineno
from pathlib import Path

import openpyxl

from src.vacancy import Vacancy
from src.utils import get_currency_rates
import logging
import pandas as pd
import csv
from openpyxl import Workbook

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
    def __init__(self, filename = f'{ROOT_DIR}\\data\\json_data.json'):
        self.__filename = filename+'.json' if filename != 'data.json' and filename[-5:] != '.json' else filename


    def read_file(self, params = None):
        vacancies = []
        data = json.load(open(self.__filename, encoding='utf-8'))

        if params is not None:
            for vacancy in data:
                currency_multiplier = 1
                is_salary: bool = (params.get('salary') is not None and
                    (vacancy['salary'] == 'Зарплата не указана' or (vacancy['salary']['from'] * currency_multiplier
                    <= params['salary'] <= vacancy['salary']['to'] * currency_multiplier)))
                is_keyword: bool = (params.get('keyword') is not None and (params['keyword'] in vacancy['name']))

                if (params.get('salary') is not None and
                        vacancy.get('salary') != 'Зарплата не указана' and
                        vacancy.get('salary').get('currency') != 'RUR'):
                    try:
                        currency_multiplier = get_currency_rates(vacancy['salary']['currency'])
                    except TypeError:
                        currency_multiplier = 1

                if params.get('keyword') is None and is_salary:
                    vacancies.append(vacancy)
                elif params.get('salary') is None and is_keyword:
                    vacancies.append(vacancy)
                elif is_salary and is_keyword:
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
                vacancies_id.append(vacancy['id'])

            for vacancy in vacancies:
                if vacancy['id'] not in vacancies_id:
                    json_data.append(vacancy)
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
    def __init__(self, filename=f'{ROOT_DIR}\\data\\excel_data.xlsx'):
        self.__filename = filename + '.xlsx' if filename != 'excel_data.xlsx' and filename[-5:] != '.xlsx' else filename

    def read_file(self, params=None):
        excel_data = pd.read_excel(self.__filename)
        data = excel_data.to_dict('records')
        vacancies = []
        if params is not None:
            for vacancy in data:
                currency_multiplier = 1
                is_salary: bool = (params.get('salary') is not None and
                    (vacancy['salary'] == 'Зарплата не указана' or (eval(vacancy['salary'])['from'] * currency_multiplier
                    <= params['salary'] <= eval(vacancy['salary'])['to'] * currency_multiplier)))
                is_keyword: bool = (params.get('keyword') is not None and (params['keyword'] in vacancy['name']))

                if (params.get('salary') is not None and
                        vacancy.get('salary') != 'Зарплата не указана' and
                        eval(vacancy.get('salary')).get('currency') != 'RUR'):
                    try:
                        currency_multiplier = get_currency_rates(eval(vacancy['salary'])['currency'])
                    except TypeError:
                        currency_multiplier = 1

                if params.get('keyword') is None and is_salary:
                    vacancies.append(vacancy)
                elif params.get('salary') is None and is_keyword:
                    vacancies.append(vacancy)
                elif is_salary and is_keyword:
                    vacancies.append(vacancy)
        else:
            for vacancy in data:
                vacancies.append(vacancy)
        return vacancies

    def save_to_file(self, vacancies):
        try:
            excel_data = pd.read_excel(self.__filename)
            vacancies_id = excel_data['id']
            for vacancy in vacancies:
                if vacancy['id'] in vacancies_id:
                    vacancies.remove(vacancy)
            fieldnames = ['id', 'name', 'salary', 'responsibility', 'requirement', 'url']
            dataframe = pd.DataFrame(data=vacancies, columns=fieldnames)
            dataframe.to_excel(self.__filename, index=False)
        except FileNotFoundError:
            fieldnames = ['id', 'name', 'salary', 'responsibility', 'requirement', 'url']
            dataframe = pd.DataFrame(data=vacancies, columns=fieldnames)
            dataframe.to_excel(self.__filename, index=False)
        except Exception as e:
            fieldnames = ['id', 'name', 'salary', 'responsibility', 'requirement', 'url']
            dataframe = pd.DataFrame(data=vacancies, columns=fieldnames)
            dataframe.to_excel(self.__filename, index=False)
            raise e


    def add_vacancy(self, vacancy):
        try:
            excel_data = pd.read_excel(self.__filename)
        except FileNotFoundError:
            raise FileNotFoundError('Файл не найден')
        vacancies_id = excel_data['id']
        data = excel_data.to_dict('records')
        if vacancy['id'] not in vacancies_id:
            data.append(vacancy)
        fieldnames = ['id', 'name', 'salary', 'responsibility', 'requirement', 'url']
        dataframe = pd.DataFrame(data=data, columns=fieldnames)
        dataframe.to_excel(self.__filename, index=False)


    def delete_vacancy(self):
        fieldnames = ['id', 'name', 'salary', 'responsibility', 'requirement', 'url']
        dataframe = pd.DataFrame(data=[], columns=fieldnames)
        dataframe.to_excel(self.__filename, index=False)


class CSVEditor(FileEditor):
    def __init__(self, filename = f'{ROOT_DIR}\\data\\csv_data.csv'):
        self.__filename = filename+'.csv' if filename != 'data.csv' and filename[-4:] != '.csv' else filename

    def read_file(self, params = None):
        vacancies = []
        with open(self.__filename, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(filter(None, reader))
            if params is not None:
                for row in data:
                    salary = row['salary']
                    currency_multiplier = 1
                    if (params.get('salary') is not None and row['salary'] != 'Зарплата не указана'):
                        salary = eval(row['salary'])
                        if salary['currency'] != 'RUR':
                            try:
                                currency_multiplier = get_currency_rates(salary['currency'])
                            except TypeError:
                                currency_multiplier = 1

                    is_salary: bool = (params.get('salary') is not None and
                                    (salary == 'Зарплата не указана' or (
                                                salary['from'] * currency_multiplier
                                                <= params['salary'] <= salary['to'] * currency_multiplier)))
                    is_keyword: bool = (params.get('keyword') is not None and (params['keyword'] in row['name']))

                    if params.get('keyword') is None and is_salary:
                        vacancies.append(row)
                    elif params.get('salary') is None and is_keyword:
                        vacancies.append(row)
                    elif is_salary and is_keyword:
                        vacancies.append(row)
            else:
                return data
        return vacancies


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
        try:
            vacancies_id = []
            with open(self.__filename, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    vacancies_id.append(row['id'])
            file_editor_logger.debug(vacancies_id)
            if vacancy['id'] not in vacancies_id:
                file_editor_logger.debug(vacancy['id'])
                with open(self.__filename, 'a', encoding='utf-8', newline='') as file:
                    file_editor_logger.debug('good')
                    fieldnames = ['id', 'name', 'salary', 'responsibility', 'requirement', 'url']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writerow(vacancy)
        except Exception as e:
            file_editor_logger.debug(e)
            with open(self.__filename, 'w', encoding='utf-8', newline='') as file:
                fieldnames = ['id', 'name', 'salary', 'responsibility', 'requirement', 'url']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(vacancy)

    def delete_vacancy(self):
        with open(self.__filename, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['id', 'name', 'salary', 'responsibility', 'requirement', 'url']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
