import pytest
import src.vacancy as vacancy

@pytest.fixture
def vacancy_data():
    vac: dict = {"name": "Разработчик фронтэнда React JS", "salary": None, "responsibility": "description",
               "requirement": "requirement", "url": "https://api.hh.ru/employers/6023237"}
    return vac

@pytest.fixture
def vacancies_list():
    vacancies_list = [
        {"name" : "name1",
         "salary" : 15000,
         "responsibility": "description1",
         "requirement": "requirement1",
         "url": "url1"},
        {"name" : "name2",
         "salary" : 20000,
         "responsibility": "description2",
         "requirement": "requirement2",
         "url": "url2"}
    ]
    return vacancies_list

def test_vacancy_validate(vacancy_data):
    vac = vacancy.Vacancy(vacancy_data)
    assert vac.salary == "Зарплата не указана"
    assert vac.url == "https://api.hh.ru/employers/6023237"
    assert vac.description == "description"
    assert vac.requirement == "requirement"
    assert vac.name == "Разработчик фронтэнда React JS"


def test_vacancy_compare(vacancies_list):
    assert vacancy.Vacancy(vacancies_list[0]) < vacancy.Vacancy(vacancies_list[1])