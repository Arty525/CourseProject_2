import pytest
from src.file_editor import FileEditor, JSONEditor
from unittest.mock import Mock, patch, mock_open
import json


@pytest.fixture
def vacancies():
    vacancies = [
            {
                "id": "117961997",
                "name": "Python разработчик",
                "salary": "Зарплата не указана",
                "url": "https://api.hh.ru/vacancies/123",
                "snippet": {
                    "requirement": "Python, Git, Docker",
                    "responsibility": "Разработка бэк-энда"
                }
            },
            {
                "id": "15213251",
                "name": "Разработчик C++",
                "salary": {"from": 150000, "to": 170000, 'currency': 'RUR'},
                "url": "https://api.hh.ru/vacancies/321",
                "snippet": {
                    "requirement": "Знание C++",
                    "responsibility": "Разработка приложений под Windows"
                }
            },
            {
                "id": "572423263",
                "name": "Уборщица",
                "salary": {'from': 25000, 'to': 30000, 'currency': "RUR"},
                "url": "https://api.hh.ru/vacancies/6612",
                "snippet": {
                    "requirement": "Умение работать со шваброй",
                    "responsibility": "Уборка офиса"
                }
            }
    ]
    return vacancies

@patch("json.load")
@patch("builtins.open")
def test_read_file(mock_open, mock_json_load, vacancies):
    mock_json_load.return_value = vacancies
    json_editor = JSONEditor()
    assert json_editor.read_file({"keyword": "Разработчик", "salary": 160000}) == [vacancies[1]]