from utils import *
from classes import *


def main():
    name_input = input("Введите свое имя: ")
    main_input = input(
        f'{name_input}, введите 1, если хотите найти вакансии "Python разработчик"'
    )

    hh = HH()
    sj = Superjob()
    hh_vacancy_list = hh.get_vacancy_list()
    sj_vacancy_list = sj.get_vacancy_list()

    vacancy = hh_vacancy_list + sj_vacancy_list
    while True:
        """
        основной цикл
        """
        print(
            '\nМеню\n'
            '1 - выбрать топ 10 вакансий по зарплате\n'
            '2 - выбрать топ вакансий  просортированные по зарплате \n'
            '3 - выбрать произвольное число по топу зарплаты\n'
            'любая другая клавиша - выход\n'
        )
        user_input = input()
        if user_input == '1':
            result = get_top(vacancy, top_count=10)
            print('Данные записались в файл')
            to_file(result)
        elif user_input == '2':
            sort_vacancy = get_sorting(vacancy)
            to_file(sort_vacancy)
        elif user_input == '3':
            top_input = int(input('Выберете кол-во вакансий'))
            top_for_number = get_top(vacancy, top_count=top_input)
            print('Данные записались в файл')
            to_file(top_for_number)
        else:
            print('Данные записались в файл')
            print("До свидания")
            to_file(vacancy)
            break


if __name__ == '__main__':
    main()
