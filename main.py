from pathlib import Path
import os.path
import src.commands as commands


ROOT_DIR = Path(__file__).parent.resolve()

if __name__ == '__main__':
    command = ''
    while command != 'нет':
        print("""Выберете команду из списка:
        1 - получить данные о вакансиях с hh.ru
        2 - выполнить поиск по вакансиям
        3 - получить ТОП вакансий по зарплате
        4 - добавить новую вакансию""")

        while command not in ['1', '2', '3', '4']:
            command = input('Введите номер команды: ')
            if command not in ['1', '2', '3', '4']:
                print('Неизвестная команда, повторите ввод\n')

        if command == '1':
            commands.get_vacancies_from_hh()

        if command == '2':
            vacancies = commands.search_vacancies()
            if len(vacancies) > 0:
                print(f'По вашему запросу найдено {len(vacancies)} вакансий.')
                command = input('Вывести результаты в txt файл? да/нет: ').lower()
                while command != 'да':
                    print('Неверная комманда, повторите ввод.\n')
                    command = input('Вывести результаты в txt файл? да/нет: ').lower()
                if command == 'да':
                    with open(os.path.join(ROOT_DIR, 'data', 'vacancies.txt'), 'w', encoding='utf-8') as file:
                        for vacancy in vacancies:
                            file.write(f'{vacancy}\n')
                else:
                    for vacancy in vacancies:
                        print(vacancy)

        if command == '3':
            vacancies = commands.get_top()
            while command.lower() not in ['да', 'нет']:
                command = input('Вывести результаты в txt файл? да/нет: ').lower()
                if command == 'да':
                    with (open(os.path.join(ROOT_DIR, 'data', f'top_{len(vacancies)}_vacancies.txt'), 'w',
                               encoding='utf-8')
                          as file):
                        for vacancy in vacancies:
                            file.write(f'{vacancy}\n')
                elif command == 'нет':
                    for vacancy in vacancies:
                        print(vacancy)
                else:
                    print('Неизвестная команда, повторите ввод\n')

        if command == '4':
            commands.add_vacancy_to_file()

        print('Выполнить другую команду?')
        command = input('Введите да или нет: ').lower()
        while command not in ['да', 'нет']:
            print('Неверная команда, повторите ввод.')
            command = input('Введите да или нет: ').lower()
