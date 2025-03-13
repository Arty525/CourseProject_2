import logging
import os
from pathlib import Path
from src.file_editor import JSONEditor, CSVEditor, ExcelEditor
from src.hh_api import HH
import random
from src.vacancy import Vacancy

ROOT_DIR = Path(__file__).resolve().parent.parent

commands_logger = logging.getLogger('commands')
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d')
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, 'logs', 'commands.log'), 'w')
file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d')
file_handler.setFormatter(file_formatter)
commands_logger.addHandler(file_handler)
commands_logger.addHandler(console_handler)
commands_logger.setLevel(logging.DEBUG)

def get_top() -> list:
    print('Вы выбрали получение ТОП-вакансий по зарплате')
    number = int(input('Введите количество вакансий в выборке: '))
    top_vacancies = []
    print(f'Выполняется выборка из {number} вакансий')
    try:
        json_editor = JSONEditor()
        vacancies = json_editor.read_file()
        for vacancy in vacancies:
            if vacancy.get('salary') != 'Зарплата не указана':
                top_vacancies.append(vacancy)
        top_vacancies = sorted(top_vacancies, key=lambda vacancy: vacancy.get('salary').get('to'), reverse=True)
        return top_vacancies[:number]
    except FileNotFoundError:
        try:
            csv_editor = CSVEditor()
            vacancies = csv_editor.read_file()
            for vacancy in vacancies:
                if vacancy.get('salary') != 'Зарплата не указана':
                    top_vacancies.append(vacancy)
            top_vacancies = sorted(top_vacancies, key=lambda vacancy: vacancy.get('salary').get('to'), reverse=True)
            return top_vacancies[:number]
        except FileNotFoundError:
            try:
                excel_editor = ExcelEditor()
                vacancies = excel_editor.read_file()
                for vacancy in vacancies:
                    if vacancy.get('salary') != 'Зарплата не указана':
                        top_vacancies.append(vacancy)
                top_vacancies = sorted(top_vacancies, key=lambda vacancy: vacancy.get('salary').get('to'), reverse=True)
                return top_vacancies[:number]
            except FileNotFoundError:
                raise FileNotFoundError('Файл не найден')

def get_vacancies_from_hh():
    print('Вы выбрали получение данных с hh.ru')
    keyword = input('Введите ключевые слова для поиска: ')
    hh_api = HH()
    try:
        data = hh_api.get_vacancies(keyword)
        print('Данные успешно получены')
    except ConnectionError:
        print('Не удалось установить соединение с hh.ru')
        raise ConnectionError
    if data is None or data == []:
        print('Не удалось получить вакансии по вашему запросу')
    # JSON
    try:
        json_editor = JSONEditor()
        json_editor.save_to_file(data)
        print('Данные сохранены в JSON-файл')
    except Exception as e:
        print(f'Не удалось сохранить данные в JSON-файл. Возникла ошибка: {e}')
        raise e
    finally:
        # CSV
        try:
            csv_editor = CSVEditor()
            csv_editor.save_to_file(data)
            print('Данные сохранены в CSV-файл')
        except Exception as e:
            print(f'Не удалось сохранить данные в CSV-файл. Возникла ошибка: {e}')
            raise e
        finally:
            # EXCEL
            try:
                excel_editor = ExcelEditor()
                excel_editor.save_to_file(data)
                print('Данные сохранены в EXCEL-файл')
            except Exception as e:
                print(f'Не удалось сохранить данные в EXCEL-файл. Возникла ошибка: {e}')
                raise e
    print('Данные успешно сохранены в папку data')


def search_vacancies()->list:
    print('Вы выбрали поиск по вакансиям')
    file_type = input('Введите тип файла для поиска (json, csv, excel): ').lower()
    print('Введите параметры для поиска или оставьте поле пустым')
    salary = int(input('Введите зарплату в рублях: '))
    keyword = input('Введите ключевое слово: ').lower()
    params = {'keyword': keyword,'salary': salary}
    vacancies = []
    if 'csv' in file_type:
        csv_reader = CSVEditor()
        vacancies = csv_reader.read_file(params)
        if vacancies is None or vacancies == []:
            print('Не удалось найти вакансии по вашему запросу')
            return []
    elif 'json' in file_type:
        json_reader = JSONEditor()
        vacancies = json_reader.read_file(params)
        if vacancies is None or vacancies == []:
            print('Не удалось найти вакансии по вашему запросу')
            return []
    elif 'excel' in file_type:
        excel_reader = ExcelEditor()
        vacancies = excel_reader.read_file(params)
        if vacancies is None or vacancies == []:
            print('Не удалось найти вакансии по вашему запросу')
            return []
    else:
        json_reader = JSONEditor()
        vacancies = json_reader.read_file(params)
        if vacancies is None or vacancies == []:
            print('Не удалось найти вакансии по вашему запросу')
            return []
    return vacancies

def add_vacancy_to_file():
    print('Вы выбрали добавление вакансии в файл')
    print('Введите данные или оставьте поле пустым')
    name = input('Введите название вакансии: ')
    responsibility = input('Введите описание вакансии: ')
    requirement = input('Введите требуемые навыки: ')
    salary_from = input('Введите зарплату от: ')
    salary_to = input('Введите зарплату до: ')
    salary_currency = input('Введите валюту: ')
    id = str(random.randint(100000000, 999999999))
    url = input('Введите ссылку на вакансию: ')
    if salary_currency == ' ':
        salary_currency = 'RUR'

    if salary_from != '' and salary_to != '':
        salary = {'from': int(salary_from), 'to': int(salary_to), 'currency': salary_currency}
    elif salary_from == '' and salary_to != '':
        salary = {'from': 0, 'to': int(salary_to), 'currency': salary_currency}
    elif salary_from != '' and salary_to == '':
        salary = {'from': int(salary_from), 'to': int(salary_from), 'currency': salary_currency}
    else:
        salary = 'Зарплата не указана'


    vacancy = Vacancy({'id': id, 'name': name, 'salary': salary, 'snippet': {'responsibility': responsibility, 'requirement': requirement}, 'url': url})
    file_type = input('Выберите тип файла (json, csv, excel): ').lower()
    if 'csv' in file_type:
        csv_editor = CSVEditor()
        try:
            csv_editor.add_vacancy(vacancy.get_vacancy())
            print('Вакансия успешно добавлена')
        except Exception as e:
            raise e
    elif 'json' in file_type:
        json_editor = JSONEditor()
        try:
            json_editor.add_vacancy(vacancy.get_vacancy())
            print('Вакансия успешно добавлена')
        except Exception as e:
            raise e
    elif 'excel' in file_type:
        excel_editor = ExcelEditor()
        try:
            excel_editor.add_vacancy(vacancy.get_vacancy())
            print('Вакансия успешно добавлена')
        except Exception as e:
            raise e
    else:
        json_editor = JSONEditor()
        try:
            json_editor.add_vacancy(vacancy.get_vacancy())
            print('Вакансия успешно добавлена')
        except Exception as e:
            raise e