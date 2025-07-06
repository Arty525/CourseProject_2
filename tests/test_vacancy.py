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
    vacancies = [
        vacancy.Vacancy(
            "117961997",
            "Python разработчик",
            "Разработка бэк-энда",
            "Зарплата не указана",
            "Python, Git, Docker",
            "https://api.hh.ru/vacancies/123",
        ),
        vacancy.Vacancy(
            "15213251",
            "Разработчик C++",
            "Разработка приложений под Windows",
            {"from": 150000, "to": 170000, "currency": "RUR"},
            "Знание C++",
            "https://api.hh.ru/vacancies/321",
        ),
        vacancy.Vacancy(
            "572423263",
            "Уборщица",
            "Уборка офиса",
            {"from": 25000, "to": 30000, "currency": "RUR"},
            "Умение работать со шваброй",
            "https://api.hh.ru/vacancies/6612",
        ),
        vacancy.Vacancy(
            "572423263",
            "Уборщица",
            "Уборка офиса",
            {"from": 25000, "to": 30000, "currency": "RUR"},
            "Умение работать со шваброй",
            "https://api.hh.ru/vacancies/6612",
        ),
    ]
    return vacancies


# ready
def test_vacancy_validate():
    vac = vacancy.Vacancy(
        123,
        "Разработчик фронтэнда React JS",
        "responsibility",
        "",
        "requirement",
        "https://api.hh.ru/employers/6023237",
    )
    assert vac.id == 123
    assert vac.salary == "Зарплата не указана"
    assert vac.url == "https://api.hh.ru/employers/6023237"
    assert vac.responsibility == "responsibility"
    assert vac.requirement == "requirement"
    assert vac.name == "разработчик фронтэнда react js"


# ready
def test_vacancy_compare(vacancies_list):
    assert (vacancies_list[0] == vacancies_list[1]) == False
    assert vacancies_list[1] > vacancies_list[2]
    assert vacancies_list[2] < vacancies_list[1]
    assert vacancies_list[2] == vacancies_list[3]


def test_vacancy_str(vacancies_list, capsys):
    print(vacancies_list[0])
    captured = capsys.readouterr()
    assert captured.out == '''python разработчик
Зарплата: Зарплата не указана
Описание вакансии: Разработка бэк-энда
Требования: Python, Git, Docker
URL: https://api.hh.ru/vacancies/123
--------------------------------------------------
'''
