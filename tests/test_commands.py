import pytest
from unittest.mock import patch
from src.commands import get_vacancies_from_hh
import src.commands as commands
import requests


@pytest.fixture
def vacancies():
    vacancies = [
            {
                'id': '117961997',
                'name': 'Python разработчик',
                'salary': 'Зарплата не указана',
                'url': 'https://api.hh.ru/vacancies/123',
                'requirement': 'Python, Git, Docker',
                'responsibility': 'Разработка бэк-энда'
            },
            {
                'id': '15213251',
                'name': 'Разработчик C++',
                'salary': {'from': 150000, 'to': 170000, 'currency': 'RUR'},
                'url': 'https://api.hh.ru/vacancies/321',
                'requirement': 'Знание C++',
                'responsibility': 'Разработка приложений под Windows'
            },
            {
                'id': '572423263',
                'name': 'Уборщица',
                'salary': {'from': 250000, 'to': 300000, 'currency': 'RUR'},
                'url': 'https://api.hh.ru/vacancies/6612',
                'requirement': 'Умение работать со шваброй',
                'responsibility': 'Уборка офиса'
            },
        ]
    return vacancies


@pytest.mark.parametrize(
    "value, expected",
    [
        (
                [
                    {
                        'id': '117961997',
                        'name': 'Python разработчик',
                        'salary': 'Зарплата не указана',
                        'url': 'https://api.hh.ru/vacancies/123',
                        'requirement': 'Python, Git, Docker',
                        'responsibility': 'Разработка бэк-энда'
                    },
                    {  # 2
                        'id': '15213251',
                        'name': 'Разработчик C++',
                        'salary': {'currency': 'RUR', 'from': 150000, 'to': 170000},
                        'url': 'https://api.hh.ru/vacancies/321',
                        'requirement': 'Знание C++',
                        'responsibility': 'Разработка приложений под Windows'
                    },
                    {  # 1
                        'id': '14634623',
                        'name': 'Team-lead',
                        'salary': {'currency': 'RUR', 'from': 250000, 'to': 300000},
                        'url': 'https://api.hh.ru/vacancies/6612',
                        'requirement': 'Умение работать в команде',
                        'responsibility': 'Руководство командой разработчиков на Python'
                    },
                    {  # 3
                        'id': '572423263',
                        'name': 'Уборщица',
                        'salary': {'currency': 'RUR', 'from': 25000, 'to': 30000},
                        'url': 'https://api.hh.ru/vacancies/6612',
                        'requirement': 'Умение работать со шваброй',
                        'responsibility': 'Уборка офиса'
                    },
                    {  # 4
                        'id': '4527245747',
                        'name': 'Уборщица в офис',
                        'salary': {'currency': 'RUR', 'from': 15000, 'to': 30000},
                        'url': 'https://api.hh.ru/vacancies/6612',
                        'requirement': 'Умение работать со шваброй',
                        'responsibility': 'Уборка офиса'
                    },
                    {  # 5
                        'id': '564248225333',
                        'name': 'Уборщица на завод',
                        'salary': {'currency': 'RUR', 'from': 5000, 'to': 10000},
                        'url': 'https://api.hh.ru/vacancies/6612',
                        'requirement': 'Умение работать со шваброй',
                        'responsibility': 'Уборка цеха'
                    },
                ],
            [
                {#1
                    'id': '14634623',
                    'name': 'Team-lead',
                    'salary':{'currency': 'RUR', 'from': 250000, 'to': 300000},
                    'url': 'https://api.hh.ru/vacancies/6612',
                    'requirement': 'Умение работать в команде',
                    'responsibility': 'Руководство командой разработчиков на Python'
                },
                {#2
                    'id': '15213251',
                    'name': 'Разработчик C++',
                    'salary': {'currency': 'RUR', 'from': 150000, 'to': 170000},
                    'url': 'https://api.hh.ru/vacancies/321',
                    'requirement': 'Знание C++',
                    'responsibility': 'Разработка приложений под Windows'
                },

                {#3
                    'id': '572423263',
                    'name': 'Уборщица',
                    'salary': {'currency': 'RUR', 'from': 25000, 'to': 30000},
                    'url': 'https://api.hh.ru/vacancies/6612',
                    'requirement': 'Умение работать со шваброй',
                    'responsibility': 'Уборка офиса'
                },
                {#4
                    'id': '4527245747',
                    'name': 'Уборщица в офис',
                    'salary': {'currency': 'RUR', 'from': 15000, 'to': 30000},
                    'url': 'https://api.hh.ru/vacancies/6612',
                    'requirement': 'Умение работать со шваброй',
                    'responsibility': 'Уборка офиса'
                },
                {#5
                    'id': '564248225333',
                    'name': 'Уборщица на завод',
                    'salary': {'currency': 'RUR', 'from': 5000, 'to': 10000},
                    'url': 'https://api.hh.ru/vacancies/6612',
                    'requirement': 'Умение работать со шваброй',
                    'responsibility': 'Уборка цеха'
                },
            ]
        )
    ]
)


#ready
@patch('builtins.input')
@patch('builtins.open')
@patch('json.load')
def test_get_top(mock_load, mock_open, mock_input, value, expected):
    mock_input.return_value = 5
    mock_load.return_value = value
    assert commands.get_top() == expected


#ready
@patch('builtins.input')
@patch('builtins.open', side_effect=FileNotFoundError)
def test_get_top_file_error(mock_open, mock_input):
    mock_input.return_value = 5
    with pytest.raises(FileNotFoundError):
        commands.get_top()


#ready
@patch('builtins.input')
@patch('builtins.open')
@patch('src.file_editor.JSONEditor.save_to_file')
@patch('src.file_editor.CSVEditor.save_to_file')
@patch('src.file_editor.ExcelEditor.save_to_file')
def test_get_vacancies_from_hh(mock_save_excel, mock_save_csv, mock_save_json, mock_open, mock_input,
                               vacancies, capsys, tmpdir):
    mock_input.return_value = ''
    get_vacancies_from_hh()
    captured = capsys.readouterr()
    assert captured.out == """Вы выбрали получение данных с hh.ru
Соединение установлено
Данные успешно получены
Не удалось получить вакансии по вашему запросу
Данные сохранены в JSON-файл
Данные сохранены в CSV-файл
Данные сохранены в EXCEL-файл
Данные успешно сохранены в папку data\n"""



@patch('builtins.input')
@patch('requests.get', return_value=ConnectionError)
def test_get_vacancies_from_hh_error(mock_get, mock_input):
    with pytest.raises(ConnectionError):
        get_vacancies_from_hh()



#ready
@patch("builtins.input", side_effect=["json", 0, "разработчик"])
@patch('src.file_editor.JSONEditor.read_file', return_value=[])
def test_search_vacancies(mock_save_json, mock_input, vacancies, capsys, tmpdir):
    commands.search_vacancies()
    captured = capsys.readouterr()
    assert captured.out == """Вы выбрали поиск по вакансиям
Введите параметры для поиска или оставьте поле пустым
Не удалось найти вакансии по вашему запросу\n"""


#ready
@patch("builtins.input", side_effect=["C++ developer", 'gamedev', 'C++, git', 10000, 20000, 'RUR', '', 'json'])
@patch('src.file_editor.JSONEditor.add_vacancy')
def test_add_vacancy_to_file(mock_save_json, mock_input, vacancies, capsys, tmpdir):
    commands.add_vacancy_to_file()
    captured = capsys.readouterr()
    assert captured.out == """Вы выбрали добавление вакансии в файл
Введите данные или оставьте поле пустым
Вакансия успешно добавлена\n"""