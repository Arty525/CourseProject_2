import logging
from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parent.parent

vacancy_logger = logging.getLogger('vacancy')
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d')
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, 'logs', 'vacancy.log'), 'w')
file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d')
file_handler.setFormatter(file_formatter)
vacancy_logger.addHandler(file_handler)
vacancy_logger.addHandler(console_handler)
vacancy_logger.setLevel(logging.DEBUG)


class Vacancy:
    __slots__ = ('id', 'name', 'responsibility', 'salary', 'requirement', 'url')
    def __init__(self, vacancy: dict):
        self.id = vacancy['id']
        self.name = vacancy['name'].lower()
        self.responsibility = vacancy['snippet']['responsibility']
        self.salary = self.__validate(vacancy['salary'])
        self.requirement = vacancy['snippet']['requirement']
        self.url = vacancy['url']


    def __lt__(self, other):
        if self.salary is str:
            return True
        elif other.salary is str:
            return False
        else:
            return max(self.salary.values()) < max(other.salary.values())

    def __gt__(self, other):
        if self.salary is str:
            return False
        elif other.salary is str:
            return True
        else:
            return max(self.salary.values()) > max(other.salary.values())

    def __eq__(self, other):
        if self.salary is str:
            return False
        elif other.salary is str:
            return False
        else:
            return max(self.salary.values()) == max(other.salary.values())


    def __validate(self, salary):
        if salary == '':
            salary = 'Зарплата не указана'
        if salary is not None and salary != 'Зарплата не указана':
            if salary['from'] is None or int(salary['from']) <= 0:
                salary['from'] = 0
            if salary['to'] is None or int(salary['to']) <= 0:
                salary['to'] = 0
            return salary
        return 'Зарплата не указана'

    def get_vacancy(self):
        return {'id': self.id, 'name': self.name, 'salary': self.salary, 'responsibility': self.responsibility,
                'requirement': self.requirement, 'url': self.url}