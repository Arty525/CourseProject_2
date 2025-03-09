from abc import ABC, abstractmethod


class Vacancy:
    __slots__ = ('name', 'responsibility', 'salary', 'requirement', 'url')
    def __init__(self, vacancy: dict):
        self.name = vacancy['name']
        self.responsibility = vacancy['snippet']['responsibility']
        self.salary = self.__validate(vacancy['salary'])
        self.requirement = vacancy['snippet']['requirement']
        self.url = vacancy['url']


    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __eq__(self, other):
        return self.salary == other.salary


    def __validate(self, salary):
        if str(salary).isnumeric():
            return str(salary)
        else:
            return "Зарплата не указана"

    def get_vacancy(self):
        return {'name': self.name, 'salary': self.salary, 'responsibility': self.responsibility,
                'requirement': self.requirement, 'url': self.url}