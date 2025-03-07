import os.path
from abc import ABC, abstractmethod
import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

class FileEditor(ABC):
    @abstractmethod
    def read_file(self, file_path, params):
        pass

    @abstractmethod
    def save_to_file(self):
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, keyword):
        pass


class JSONEditor(FileEditor):
    def read_file(self, file_path, params):
        vacancies = []
        data = json.load(open(file_path, encoding='utf-8'))
        print(data)
        for vacancy in data:
            if params['keyword'] in vacancy['name'] and (params['salary'] <= vacancy['salary'] or vacancy['salary'] is None):
                vacancies.append(vacancy)

        return vacancies


    def save_to_file(self):
        with open(os.path.join(ROOT_DIR, "data", "vacancies.json"), 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
            f.close()

    def add_vacancy(self, vacancy):
        with open(os.path.join(ROOT_DIR, "data", "vacancies.json"), 'a', encoding='utf-8') as f:
            f.write(json.dumps(vacancy, ensure_ascii=False, indent=4))

    def delete_vacancy(self, keyword):
        with open(os.path.join(ROOT_DIR, "data", "vacancies.json"), 'r', encoding='utf-8') as f:
            data = json.load(f)
