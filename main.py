#1 получение информации о вакансиях через API +
#2 сохранение вакансий в файл JSON +
#3 обработка информации из файла (добавление, фильтрация, удаление)

from src.hh_api import HH
from src.file_editor import JSONEditor

if __name__ == '__main__':
    hh_api = HH()
    data = hh_api.get_vacancies("Разработчик")
    json_editor = JSONEditor(data)
    json_editor.save_to_file()