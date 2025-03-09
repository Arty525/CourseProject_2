import pytest
import src.vacancy as vacancy

@pytest.fixture
def vacancy_data():
    vac: dict = {"name": "Разработчик фронтэнда React JS", "salary": None, "responsibility": "responsibility",
               "requirement": "requirement", "url": "https://api.hh.ru/employers/6023237"}
    return vac

@pytest.fixture
def vacancies_list():
    vacancies_list = [
        {"name" : "name1",
         "salary" : 15000,
         "responsibility": "responsibility1",
         "requirement": "requirement1",
         "url": "url1"},
        {"name" : "name2",
         "salary" : 20000,
         "responsibility": "responsibility2",
         "requirement": "requirement2",
         "url": "url2"},
        {"name": "name3",
         "salary": 20000,
         "responsibility": "responsibility3",
         "requirement": "requirement3",
         "url": "url3"}
    ]
    return vacancies_list

def test_vacancy_validate(vacancy_data):
    vac = vacancy.Vacancy(vacancy_data)
    assert vac.salary == "Зарплата не указана"
    assert vac.url == "https://api.hh.ru/employers/6023237"
    assert vac.responsibility == "responsibility"
    assert vac.requirement == "requirement"
    assert vac.name == "Разработчик фронтэнда React JS"


def test_vacancy_compare(vacancies_list):
    assert vacancy.Vacancy(vacancies_list[0]) < vacancy.Vacancy(vacancies_list[1])
    assert vacancy.Vacancy(vacancies_list[1]) > vacancy.Vacancy(vacancies_list[0])
    assert vacancy.Vacancy(vacancies_list[1]) == vacancy.Vacancy(vacancies_list[2])