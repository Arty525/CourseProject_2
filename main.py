#1 получение информации о вакансиях через API +
#2 сохранение вакансий в файл JSON +
#3 обработка информации из файла (добавление, фильтрация, удаление)

from src.hh_api import HH
from src.file_editor import JSONEditor, CSVEditor
from pathlib import Path
from src.vacancy import Vacancy
import os.path
from src.utils import get_currency_rates

ROOT_DIR = Path(__file__).parent.resolve()

if __name__ == '__main__':
    hh_api = HH()
    data = hh_api.get_vacancies("Разработчик")
    json_editor = JSONEditor(os.path.join(ROOT_DIR, "data", "data.json"))
    json_editor.save_to_file(data)
    csv_editor = CSVEditor()
    csv_editor.save_to_file(data)
    salary = 90000
    keyword = "Разработчик"
    params = {'keyword': keyword, 'salary': salary}
    vacancies = json_editor.read_file(params)
    for vacancy in vacancies:
        print(vacancy['id'], vacancy['name'], vacancy['salary'])
    vacancy = Vacancy({'id': 123, 'name': 'Test vacancy', 'salary': {'from': 100, 'to': 200}, 'snippet': {'responsibility': 'test responsibility', 'requirement': 'test requirement'}, 'url': 'test url'}).get_vacancy()
    json_editor.add_vacancy(vacancy)
    params = {'keyword': 'Test'}
    vacancies = json_editor.read_file(params)
    for vacancy in vacancies:
        print(vacancy)