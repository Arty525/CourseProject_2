#1 получение информации о вакансиях через API +
#2 сохранение вакансий в файл JSON +
#3 обработка информации из файла (добавление, фильтрация, удаление)

from src.hh_api import HH
from src.file_editor import JSONEditor, CSVEditor, ExcelEditor
from pathlib import Path
from src.vacancy import Vacancy
import os.path
import json
from src.utils import get_currency_rates

ROOT_DIR = Path(__file__).parent.resolve()

if __name__ == '__main__':
    # hh_api = HH()
    # data = hh_api.get_vacancies("Разработчик")
    # with open('data/api_data.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)
    data = json.load(open('data/api_data.json', 'r', encoding='utf-8'))
    # #JSON
    json_editor = JSONEditor()
    json_editor.save_to_file(data)
    #CSV
    # csv_editor = CSVEditor()
    # csv_editor.save_to_file(data)
    #EXCEL
    # excel_editor = ExcelEditor()
    # excel_editor.save_to_file(data)
    #
    # salary = 90000
    # keyword = "Разработчик"
    # params = {'keyword': keyword, 'salary': salary}
    #
    # vacancies = json_editor.read_file(params)
    # with open('data/from_json.txt', 'w', encoding='utf-8') as f:
    #     for vacancy in vacancies:
    #         f.write(f'{vacancy['id']} {vacancy['name']} {vacancy['salary']}\n')
    #
    # vacancies = csv_editor.read_file(params)
    # with open('data/from_csv.txt', 'w', encoding='utf-8') as f:
    #     for vacancy in vacancies:
    #         f.write(f'{vacancy['id']} {vacancy['name']} {vacancy['salary']}\n')
    #
    # vacancies = excel_editor.read_file(params)
    # with open('data/from_excel.txt', 'w', encoding='utf-8') as f:
    #     for vacancy in vacancies:
    #         f.write(f'{vacancy['id']} {vacancy['name']} {vacancy['salary']}\n')

    vacancy = Vacancy({'id': '123', 'name': 'Test vacancy', 'salary': {'from': 100, 'to': 200, 'currency': 'RUR', 'gross': False}, 'snippet': {'responsibility': 'test responsibility', 'requirement': 'test requirement'}, 'url': 'test url'}).get_vacancy()
    #
    json_editor.add_vacancy(vacancy)
    #
    # csv_editor.add_vacancy(vacancy)
    #
    # excel_editor.add_vacancy(vacancy)