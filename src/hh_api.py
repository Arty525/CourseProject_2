from abc import ABC, abstractmethod
from urllib.error import HTTPError

import requests
import logging
from pathlib import Path
import os
from src.vacancy import Vacancy
from requests import TooManyRedirects

from tests.test_vacancy import vacancies_list

ROOT_DIR = Path(__file__).resolve().parent.parent

hh_api_logger = logging.getLogger('hh_api')
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d')
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, 'logs', 'hh_api.log'), 'w')
file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(name)s - %(message)s - %(pathname)s:%(lineno)d')
file_handler.setFormatter(file_formatter)
hh_api_logger.addHandler(file_handler)
hh_api_logger.addHandler(console_handler)
hh_api_logger.setLevel(logging.DEBUG)


class HeadHunterAPI(ABC):
    @abstractmethod
    def _connect_api(self):
        pass

    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class HH(HeadHunterAPI):
    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__base_url = 'https://api.hh.ru/'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []

    def _connect_api(self):
        try:
            response = requests.get(self.__base_url, headers=self.__headers)
            result = f'{response.status_code} {response.reason}'
            print('Соединение установлено')
            return True
        except requests.exceptions.ConnectionError:
            result = f'{response.status_code} {response.reason}'
            hh_api_logger.error(result)
            raise ConnectionError
        except requests.exceptions.Timeout:
            result = f'{response.status_code} {response.reason}'
            hh_api_logger.error(result)
            raise TimeoutError
        except requests.exceptions.RequestException:
            result = f'{response.status_code} {response.reason}'
            hh_api_logger.error(result)
            raise ConnectionError
        except requests.exceptions.HTTPError:
            result = f'{response.status_code} {response.reason}'
            hh_api_logger.error(result)
            raise HTTPError
        except requests.exceptions.TooManyRedirects:
            result = f'{response.status_code} {response.reason}'
            hh_api_logger.error(result)
            raise TooManyRedirects

    def get_vacancies(self, keyword):
        try:
            self._connect_api()
        except Exception as e:
            hh_api_logger.error(e)
            raise e
        else:
            self._connect_api()
            self.__params['text'] = keyword
            while self.__params.get('page') != 20:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                vacancies = response.json()['items']
                self.__vacancies.extend(vacancies)
                self.__params['page'] += 1
        finally:
            vacancies_list = []
            for vacancy in self.__vacancies:
                vacancies_list.append(Vacancy(vacancy).get_vacancy())
            return vacancies_list