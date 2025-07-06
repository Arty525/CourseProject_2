import csv
import json
from unittest.mock import patch

import pandas as pd
import pytest

from src.file_editor import CSVEditor, ExcelEditor, JSONEditor
from src.vacancy import Vacancy


@pytest.fixture
def vacancies():
    vacancies = [
        {
            "id": "117961997",
            "name": "python разработчик",
            "salary": "Зарплата не указана",
            "url": "https://api.hh.ru/vacancies/123",
            "requirement": "Python, Git, Docker",
            "responsibility": "Разработка бэк-энда",
        },
        {
            "id": "15213251",
            "name": "разработчик c++",
            "salary": {"from": 150000, "to": 170000, "currency": "RUR"},
            "url": "https://api.hh.ru/vacancies/321",
            "requirement": "Знание C++",
            "responsibility": "Разработка приложений под Windows",
        },
        {
            "id": "572423263",
            "name": "уборщица",
            "salary": {"from": 25000, "to": 30000, "currency": "RUR"},
            "url": "https://api.hh.ru/vacancies/6612",
            "requirement": "Умение работать со шваброй",
            "responsibility": "Уборка офиса",
        },
    ]
    return vacancies


@pytest.fixture
def vacancies_obj():
    vacancies = [
        Vacancy(
            "117961997",
            "Python разработчик",
            "Разработка бэк-энда",
            "Зарплата не указана",
            "Python, Git, Docker",
            "https://api.hh.ru/vacancies/123",
        ),
        Vacancy(
            "15213251",
            "Разработчик C++",
            "Разработка приложений под Windows",
            {"from": 150000, "to": 170000, "currency": "RUR"},
            "Знание C++",
            "https://api.hh.ru/vacancies/321",
        ),
        Vacancy(
            "572423263",
            "Уборщица",
            "Уборка офиса",
            {"from": 25000, "to": 30000, "currency": "RUR"},
            "Умение работать со шваброй",
            "https://api.hh.ru/vacancies/6612",
        ),
    ]
    return vacancies


# JSON TESTS
@patch("json.load")
@patch("builtins.open")
def test_read_json_file(mock_open, mock_json_load, vacancies, vacancies_obj):
    mock_open()
    mock_json_load.return_value = vacancies
    json_editor = JSONEditor()
    result = json_editor.read_file({"keyword": "Разработчик", "salary": ""})
    assert result[0].id == "117961997"
    assert result[1].id == "15213251"
    assert len(result) == 2

    result = json_editor.read_file({"keyword": "Разработчик", "salary": 160000})
    assert result[0].id == "117961997"
    assert result[1].id == "15213251"
    assert len(result) == 2
    assert (
        json_editor.read_file({"keyword": "Уборщица", "salary": ""})[0].id
        == vacancies_obj[2].id
    )
    assert json_editor.read_file({"keyword": "Уборщица", "salary": 50000}) == []


def test_read_json_file_error(vacancies):
    json_editor = JSONEditor("noname.json")
    with pytest.raises(FileNotFoundError):
        json_editor.read_file({})


def test_save_to_json_file(vacancies, vacancies_obj, tmpdir):
    file = tmpdir.join("output.json")
    json_editor = JSONEditor(str(file))
    json_editor.save_to_file(vacancies_obj)
    with open(file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    assert json_data == vacancies


@patch("json.load")
@patch("builtins.open")
def test_add_vacancy_to_json_file(
    mock_open, mock_json_load, vacancies, vacancies_obj, tmpdir
):
    mock_open()
    mock_json_load.return_value = [vacancies[0], vacancies[2]]
    file = tmpdir.join("output.json")
    json_editor = JSONEditor(str(file))
    json_editor.add_vacancy(vacancies_obj[1])
    with open(file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    assert json_data[0] == vacancies[0]
    assert json_data[1] == vacancies[2]
    assert json_data[2] == vacancies[1]


def test_delete_vacancy_json(vacancies, vacancies_obj, tmpdir):
    file = tmpdir.join("output.json")
    json_editor = JSONEditor(str(file))
    json_editor.save_to_file(vacancies_obj)
    with open(file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    assert json_data == vacancies
    json_editor.delete_vacancy()
    with open(file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    assert json_data == []


# EXCEL TESTS
@patch("pandas.read_excel")
@patch("builtins.open")
def test_read_excel_file(mock_open, mock_read_excel, vacancies, vacancies_obj):
    mock_open()
    fieldnames = ["id", "name", "salary", "responsibility", "requirement", "url"]
    mock_read_excel.return_value = pd.DataFrame(vacancies, columns=fieldnames)
    excel_editor = ExcelEditor()
    result = excel_editor.read_file({"keyword": "Разработчик", "salary": ""})
    assert result[0].id == "117961997"
    assert result[1].id == "15213251"
    assert len(result) == 2

    result = excel_editor.read_file({"keyword": "Разработчик", "salary": 160000})
    assert result[0].id == "117961997"
    assert result[1].id == "15213251"
    assert len(result) == 2
    assert (
        excel_editor.read_file({"keyword": "Уборщица", "salary": ""})[0].id
        == vacancies_obj[2].id
    )
    assert excel_editor.read_file({"keyword": "Уборщица", "salary": 50000}) == []


def test_save_to_excel_file(vacancies, vacancies_obj, tmpdir):
    file = tmpdir.join("output.xlsx")
    excel_editor = ExcelEditor(str(file))
    excel_editor.save_to_file(vacancies_obj)
    excel_data = pd.read_excel(str(file)).to_dict("records")
    assert excel_data[0]["name"] == vacancies[0]["name"]
    assert excel_data[0]["salary"] == vacancies[0]["salary"]
    assert excel_data[0]["responsibility"] == vacancies[0]["responsibility"]
    assert excel_data[1]["name"] == vacancies[1]["name"]


def test_add_vacancy_to_excel_file(vacancies, vacancies_obj, tmpdir):
    file = tmpdir.join("output.xlsx")
    fieldnames = ["id", "name", "salary", "responsibility", "requirement", "url"]
    pd.DataFrame([vacancies[0], vacancies[2]], columns=fieldnames).to_excel(str(file))
    excel_editor = ExcelEditor(str(file))
    excel_editor.add_vacancy(vacancies_obj[1])
    excel_data = pd.read_excel(str(file)).to_dict("records")
    assert excel_data[2]["name"] == vacancies[1]["name"]


def test_delete_vacancy_excel(vacancies, vacancies_obj, tmpdir):
    file = tmpdir.join("output.xlsx")
    excel_editor = ExcelEditor(str(file))
    excel_editor.save_to_file(vacancies_obj)
    excel_data = pd.read_excel(str(file)).to_dict("records")
    assert excel_data[0]["name"] == vacancies[0]["name"]
    excel_editor.delete_vacancy()
    excel_data = pd.read_excel(str(file)).to_dict("records")
    assert excel_data == []


# CSV TESTS
def test_read_csv_file(vacancies, vacancies_obj, tmpdir):
    file = tmpdir.join("output.csv")
    csv_editor = CSVEditor(str(file))
    csv_editor.save_to_file(vacancies_obj)
    csv_data = list(csv.DictReader(open(file, "r", encoding="utf-8")))
    assert csv_data[0]["name"] == vacancies[0]["name"]
    assert csv_data[1]["name"] == vacancies[1]["name"]
    assert csv_data[2]["name"] == vacancies[2]["name"]
    assert csv_data[0] == vacancies[0]


def test_read_csv_file_error():
    csv_editor = CSVEditor("noname.csv")
    with pytest.raises(FileNotFoundError):
        csv_editor.read_file({})


def test_save_to_csv_file(vacancies, vacancies_obj, tmpdir):
    file = tmpdir.join("output.csv")
    csv_editor = CSVEditor(str(file))
    csv_editor.save_to_file(vacancies_obj)
    csv_data = list(csv.DictReader(open(file, "r", encoding="utf-8")))
    assert csv_data[0]["name"] == vacancies[0]["name"]
    assert csv_data[0]["salary"] == vacancies[0]["salary"]
    assert csv_data[0]["responsibility"] == vacancies[0]["responsibility"]
    assert csv_data[1]["name"] == vacancies[1]["name"]


def test_add_vacancy_to_csv_file(vacancies, vacancies_obj, tmpdir):
    file = tmpdir.join("output.csv")
    csv_editor = CSVEditor(str(file))
    csv_editor.save_to_file([vacancies_obj[0], vacancies_obj[2]])
    csv_editor.add_vacancy(vacancies_obj[1])
    csv_data = list(csv.DictReader(open(file, "r", encoding="utf-8")))
    assert csv_data[2]["name"] == vacancies[1]["name"]


def test_delete_vacancy_csv(vacancies, vacancies_obj, tmpdir):
    file = tmpdir.join("output.csv")
    csv_editor = CSVEditor(str(file))
    csv_editor.save_to_file(vacancies_obj)
    csv_data = list(csv.DictReader(open(file, "r", encoding="utf-8")))
    assert csv_data[0] == vacancies[0]
    csv_editor.delete_vacancy()
    csv_data = list(csv.DictReader(open(file, "r", encoding="utf-8")))
    assert csv_data == []
