from abc import ABC, abstractmethod


class Vacancy:
    __slots__ = ('name', 'description', 'salary', 'requirement', 'url')
    def __init__(self, vacancy: dict):
        self.name = vacancy['name']
        self.description = vacancy['responsibility']
        self.salary = self.__validate(vacancy['salary'])
        self.requirement = vacancy['requirement']
        self.url = vacancy['url']


    def __lt__(self, other):
        return self.salary < other.salary


    def __validate(self, salary):
        if str(salary).isnumeric():
            return str(salary)
        else:
            return "Зарплата не указана"