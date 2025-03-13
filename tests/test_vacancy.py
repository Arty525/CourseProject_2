import pytest

import src.vacancy as vacancy


@pytest.fixture
def vacancy_data():
    vac: dict = {
        "id": 123,
        "name": "Разработчик фронтэнда React JS",
        "salary": "",
        "snippet": {"responsibility": "responsibility", "requirement": "requirement"},
        "url": "https://api.hh.ru/employers/6023237",
    }
    return vac


@pytest.fixture
def vacancies_list():
    vacancies_list = [
        {
            "id": 1,
            "name": "name1",
            "salary": {"from": 10000, "to": 15000},
            "snippet": {
                "responsibility": "responsibility1",
                "requirement": "requirement1",
            },
            "url": "url1",
        },
        {
            "id": 2,
            "name": "name2",
            "salary": {"from": None, "to": 20000},
            "snippet": {
                "responsibility": "responsibility2",
                "requirement": "requirement2",
            },
            "url": "url2",
        },
        {
            "id": 3,
            "name": "name3",
            "salary": {"from": None, "to": 20000},
            "snippet": {
                "responsibility": "responsibility3",
                "requirement": "requirement3",
            },
            "url": "url3",
        },
        {
            "id": 4,
            "name": "name4",
            "salary": {"from": 10000, "to": 15000},
            "snippet": {
                "responsibility": "responsibility4",
                "requirement": "requirement4",
            },
            "url": "url4",
        },
    ]
    return vacancies_list


# ready
def test_vacancy_validate(vacancy_data):
    vac = vacancy.Vacancy(vacancy_data)
    assert vac.id == 123
    assert vac.salary == "Зарплата не указана"
    assert vac.url == "https://api.hh.ru/employers/6023237"
    assert vac.responsibility == "responsibility"
    assert vac.requirement == "requirement"
    assert vac.name == "разработчик фронтэнда react js"


# ready
def test_vacancy_compare(vacancies_list):
    assert vacancy.Vacancy(vacancies_list[0]) < vacancy.Vacancy(vacancies_list[1])
    assert vacancy.Vacancy(vacancies_list[1]) > vacancy.Vacancy(vacancies_list[0])
    assert vacancy.Vacancy(vacancies_list[1]) == vacancy.Vacancy(vacancies_list[2])
    assert vacancy.Vacancy(vacancies_list[0]) == vacancy.Vacancy(vacancies_list[3])
