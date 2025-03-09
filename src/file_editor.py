import os.path
from abc import ABC, abstractmethod
import json
from pathlib import Path
from src.vacancy import Vacancy
from src.utils import get_currency_rates
import logging

ROOT_DIR = Path(__file__).resolve().parent.parent


file_editor_logger = logging.getLogger("file_editor")
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", "file_editor.log"), "w")
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d")
file_handler.setFormatter(file_formatter)
file_editor_logger.addHandler(file_handler)
file_editor_logger.addHandler(console_handler)
file_editor_logger.setLevel(logging.DEBUG)

class FileEditor(ABC):
    @abstractmethod
    def read_file(self, params):
        pass

    @abstractmethod
    def save_to_file(self):
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass


class JSONEditor(FileEditor):
    def __init__(self, filename = "vacancies.json", vacancies = None):
        self._vacancies = vacancies
        self.__filename = filename

    def read_file(self, params = None):
        vacancies = []
        data = json.load(open(self.__filename, encoding='utf-8'))
        if params is not None:
            for vacancy in data:
                currency_multiplier = 1
                file_editor_logger.debug(vacancy['salary'])
                if vacancy.get('salary') != 'Зарплата не указана' and vacancy.get('salary').get('currency') != 'RUR':
                    try:
                        currency_multiplier = get_currency_rates(vacancy['salary']['currency'])
                    except TypeError:
                        currency_multiplier = 1
                if ((params['keyword'] in vacancy['name'] or params['keyword'] in vacancy['snippet']['requirement'])
                        and (vacancy['salary'] == "Зарплата не указана"
                             or (vacancy['salary']['from'] * currency_multiplier <= params['salary']
                                 <= vacancy['salary']['to'] * currency_multiplier))):
                    vacancies.append(vacancy)
        else:
            for vacancy in data:
                vacancies.append(vacancy)
        return vacancies


    def save_to_file(self):
        with open(os.path.join(ROOT_DIR, "data", self.__filename), 'w', encoding='utf-8') as f:
            json.dump(self._vacancies, f, ensure_ascii=False, indent=4)
        f.close()

    def add_vacancy(self, vacancy):
        with open(os.path.join(ROOT_DIR, "data", self.__filename), 'a', encoding='utf-8') as f:
            f.write(json.dumps(vacancy, ensure_ascii=False, indent=4))

    def delete_vacancy(self):
        open(os.path.join(ROOT_DIR, "data", self.__filename), 'w', encoding='utf-8').close()
