from pathlib import Path
import os.path
import src.commands as commands


ROOT_DIR = Path(__file__).parent.resolve()

if __name__ == '__main__':
    print("""Выберете команду из списка:
    1 - получить данные о вакансиях с hh.ru
    2 - выполнить поиск по вакансиям
    3 - получить ТОП вакансий по зарплате
    4 - добавить новую вакансию""")

    command = input('Введите номер команды: ')

    if command == '1':
        commands.get_vacancies_from_hh()

    if command == '2':
        vacancies = commands.search_vacancies()
        if len(vacancies) > 0:
            print(f'По вашему запросу найдено {len(vacancies)} вакансий.')
            if input('Вывести результаты в txt файл? да/нет: ').lower() == 'да':
                with open(os.path.join(ROOT_DIR, 'data', 'vacancies.txt'), 'w', encoding='utf-8') as file:
                    for vacancy in vacancies:
                        file.write(f'{vacancy}\n')
            else:
                print(vacancies)

    if command == '3':
        vacancies = commands.get_top()
        if input('Вывести результаты в txt файл? да/нет: ').lower() == 'да':
            with (open(os.path.join(ROOT_DIR, 'data', f'top_{len(vacancies)}_vacancies.txt'), 'w', encoding='utf-8')
                  as file):
                for vacancy in vacancies:
                    file.write(f'{vacancy}\n')
        else:
            print(vacancies)

    if command == '4':
        commands.add_vacancy_to_file()
