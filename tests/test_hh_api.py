import requests
import src.hh_api as hh_api
import pytest
from unittest.mock import Mock, patch, mock_open
import json


#ready
@patch('requests.get')
def test_connect_api_code_200(mock_get):
    mock_get.return_value.status_code = 200
    api_obj = hh_api.HH()
    assert api_obj._connect_api() == True


#ready
@patch('requests.get')
def test_connect_api_connection_error(mock_get):
    mock_get.side_effect = ConnectionError
    api_obj = hh_api.HH()
    with pytest.raises(ConnectionError):
        api_obj._connect_api()


#ready
@patch('requests.get')
def test_connect_api_timeout_error(mock_get):
    mock_get.side_effect = TimeoutError
    api_obj = hh_api.HH()
    with pytest.raises(TimeoutError):
        api_obj._connect_api()


#ready
@patch('requests.get')
def test_connect_api_http_error(mock_get):
    mock_get.side_effect = requests.exceptions.HTTPError
    api_obj = hh_api.HH()
    with pytest.raises(requests.exceptions.HTTPError):
        api_obj._connect_api()


#ready
@patch('requests.get')
def test_connect_api_too_many_redirects(mock_get):
    mock_get.side_effect = requests.exceptions.TooManyRedirects
    api_obj = hh_api.HH()
    with pytest.raises(requests.exceptions.TooManyRedirects):
        api_obj._connect_api()


@pytest.fixture
def request_result():
    result = {"items":
                  [
                      {
                          "id":"93353083",
                          "premium":False,
                          "name":"Тестировщик комфорта квартир",
                          "department":None,
                          "has_test":False,
                          "response_letter_required":False,
                          "area":
                              {
                                  "id":"26",
                                  "name":"Воронеж",
                                  "url":"https://api.hh.ru/areas/26"},
                          "salary":
                              {
                                  "from":350000,
                                  "to":450000,
                                  "currency":"RUR",
                                  "gross":False
                              },
                          "type":
                              {
                                  "id":"open",
                                  "name":"Открытая"
                              },
                          "address":None,
                          "response_url":None,
                          "sort_point_distance":None,
                          "published_at":"2024-02-16T14:58:28+0300",
                          "created_at":"2024-02-16T14:58:28+0300",
                          "archived":False,
                          "apply_alternate_url":"https://hh.ru/applicant/vacancy_response?vacancyId=93353083",
                          "branding":
                              {
                                  "type":"CONSTRUCTOR",
                                  "tariff":"BASIC"
                              },
                          "show_logo_in_search":False,
                          "insider_interview":None,
                          "url":"https://api.hh.ru/vacancies/93353083?host=hh.ru",
                          "alternate_url":"https://hh.ru/vacancy/93353083",
                          "relations":[],
                          "employer":
                              {
                                  "id":"3499705",
                                  "name":"Специализированный застройщик BM GROUP",
                                  "url":"https://api.hh.ru/employers/3499705",
                                  "alternate_url":"https://hh.ru/employer/3499705",
                                  "logo_urls":
                                      {
                                          "original":"https://hhcdn.ru/employer-logo-original/1214854.png",
                                          "240":"https://hhcdn.ru/employer-logo/6479866.png",
                                          "90":"https://hhcdn.ru/employer-logo/6479865.png"
                                      },
                                  "vacancies_url":"https://api.hh.ru/vacancies?employer_id=3499705",
                                  "accredited_it_employer":False,
                                  "trusted":None
                              },
                          "snippet":
                              {
                                  "requirement":"Занимать активную жизненную позицию, уметь активно танцевать и громко "
                                                "петь. Обладать навыками коммуникации, чтобы налаживать добрососедские "
                                                "отношения. Обладать системным мышлением...",
                                  "responsibility":"Оценивать вид из окна: встречать рассветы на кухне, и провожать "
                                                   "алые закаты в спальне. Оценивать инфраструктуру района: ежедневно "
                                                   "ходить на..."
                              },
                          "contacts":None,
                          "schedule":
                              {
                                  "id":"flexible",
                                  "name":"Гибкий график"
                              },
                          "working_days":[],
                          "working_time_intervals":[],
                          "working_time_modes":[],
                          "accept_temporary":False,
                          "professional_roles":
                              [
                                  {
                                      "id":"107",
                                      "name":"Руководитель проектов"
                                  }
                              ],
                          "accept_incomplete_resumes":False,
                          "experience":
                              {
                                  "id":"noExperience",
                                  "name":"Нет опыта"
                              },
                          "employment":
                              {
                                  "id":"full",
                                  "name":"Полная занятость"
                              },
                          "adv_response_url":None,
                          "is_adv_vacancy":False,
                          "adv_context":None
                      }
        ],
        "found": 1, "pages": 0, "page": 0, "per_page": 0, "clusters": None, "arguments": None, "fixes": None,
        "suggests": None, "alternate_url": "https://hh.ru/search/vacancy?enable_snippets=true"
    }
    return result


#ready
@patch('requests.get')
def test_get_vacancies(mock_get, request_result):
    mock_get.return_value.json.return_value = request_result
    vacancies = hh_api.HH().get_vacancies('')
    vacancy = vacancies[0]
    assert vacancy['id'] == '93353083'
    assert vacancy['name'] == 'тестировщик комфорта квартир'
    assert vacancy['salary']['from'] == 350000
    assert vacancy['salary']['to'] == 450000
    assert vacancy['salary']['currency'] == 'RUR'