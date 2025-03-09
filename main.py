#1 получение информации о вакансиях через API +
#2 сохранение вакансий в файл JSON +
#3 обработка информации из файла (добавление, фильтрация, удаление)

from src.hh_api import HH
from src.file_editor import JSONEditor
from pathlib import Path
import os.path
from src.utils import get_currency_rates

ROOT_DIR = Path(__file__).parent.resolve()

if __name__ == '__main__':
    # hh_api = HH()
    # data = hh_api.get_vacancies("Разработчик")
    json_editor = JSONEditor(os.path.join(ROOT_DIR, "data", "vacancies.json"))
    #json_editor.save_to_file()
    salary = 90000
    keyword = "Разработчик"
    params = {'keyword': keyword, 'salary': salary}
    vacancies = json_editor.read_file(params)
    print(vacancies)