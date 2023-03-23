import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

import requests

from utils import *


class Engine(ABC):

    @abstractmethod
    def get_request(self, url: str, params: dict, headers=None):
        """
        Абстрактный метеод принимающий ссылку и параметры и отдающий данные
        """

        if headers is None:
            response = requests.get(url=url, params=params)
        else:
            response = requests.get(url=url, params=params, headers=headers)
        return response

    @staticmethod
    def get_connector(file_name):
        pass


class HH(Engine):

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies/'
        self.__params = {'text': f'Name:Python', 'per_page': 100, 'area': '113'}

    def get_request(self):
        """
        Переобразовывает ссылку в формат списка джисон
        """
        return super().get_request(url=self.__url, params=self.__params).json()

    def get_formatted_data(self, unformatted_data):
        """
        Форматирует данные для удобной работы с ними

        """

        about_vacancy = {
            'site_name': 'HH.ru',
            'name': get_name_hh(unformatted_data),
            'url': get_url_hh(unformatted_data),
            'discription': get_discription_hh(unformatted_data),
            'salary': get_salary_hh(unformatted_data),
            'city': get_city_hh(unformatted_data)

        }
        return about_vacancy

    def get_vacancy_list(self):
        """
        Метод получает готовый лист вакансий

        """
        vacancy_list = []
        page = 0

        while True:
            self.__params['page'] = page
            data = self.get_request()
            for item in data.get('items'):
                vacancy_list.append(Vacancy(data=self.get_formatted_data(unformatted_data=item)))
            if len(vacancy_list) == 500:
                print(f'Всего вакансий C hh.ru - {len(vacancy_list)}')
                break
            else:
                page += 1
        return vacancy_list


class Superjob(Engine):

    def __init__(self):
        self.my_auth_data = {
            'X-Api-App-Id': 'v3.r.137417367.c9eaf0a7d9ee18a7194f5c2b75fa46c86b533977.0146fbc82574c0cec8667869d1e560f196632d85'}
        self.__url = 'https://api.superjob.ru/2.0/vacancies'
        self.__params = {"keywords": 'Python', "count": 100}

    def get_request(self):
        """
                Переобразовывает ссылку в формат списка джисон
                """
        return super().get_request(url=self.__url, params=self.__params, headers=self.my_auth_data).json()

    def get_formatted_data(self, unformatted_data):
        """
        Форматирует данные для удобной работы с ними

        """

        about_vacancy = {
            'site_name': 'Superjob.ru',
            'name': get_name_sj(unformatted_data),
            'url': get_url_sj(unformatted_data),
            'discription': get_discription_sj(unformatted_data),
            'salary': get_salary_sj(unformatted_data),
            'city': get_city_sj(unformatted_data)

        }

        return about_vacancy

    def get_vacancy_list(self):

        vacancy_list = []
        page = 1
        while True:
            self.__params = {"keywords": 'Python', 'page': page, "count": 100}

            data = self.get_request()
            for item in data.get('objects'):
                vacancy_list.append(SJVacancy(data=self.get_formatted_data(unformatted_data=item)))
            page += 1

            if page == 6:
                print(f'Всего вакансий с superjob.ru- {len(vacancy_list)}')
                break

        return vacancy_list


class Vacancy:
    __slots__ = ['data']

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f'\n {self.name}, зарплата {self.salary},\nОписание: {self.discription},\nСсылка: {self.url}\nГород: {self.city}\n'

    @property
    def name(self):
        name = self.data['name']
        return name

    @property
    def url(self):
        url = self.data['url']
        return url

    @property
    def discription(self):
        discription = self.data['discription']
        return discription

    @property
    def salary(self):
        salary = self.data['salary']
        return salary

    @property
    def city(self):
        city = self.data['city']
        return city


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, file_path: str):
        self.__data_file = file_path

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        return self.__data_file

        # тут должен быть код для установки файла

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных

        """
        try:
            with open(self.__data_file, "r") as f:
                json.load(f)
        except FileNotFoundError:
            with open(self.__data_file, 'w') as f:
                json.dump([], f)
        except json.JSONDecodeError:
            raise Exception('Json-файл поврежден!')

    def insert(self, new_data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        self.__connect()
        with open(self.__data_file, 'r', encoding='utf8') as f:
            data = json.load(f)
        data.append(new_data)

        with open(self.__data_file, 'w') as f:
            json.dump(data, f)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        with open(self.__data_file, 'r') as f:
            data = json.load(f)
        if not query:
            return data

        data_from_file = []
        for item in data:
            for key, value in query.items():
                if item[key] == value:
                    data_from_file.append(item)
        return data

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        with open(self.__data_file, encoding="utf8") as file:
            data = json.load(file)
        with open(self.__data_file, "w", encoding="utf8") as file:
            data = list(filter(lambda item: not all(item[key] == value for key, value in query.items()), data))
            json.dump(data, file, indent=2)


class CountMixin:

    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        with open("vacancy.json", "r") as fh:
            data = json.load(fh)
            return len(data)


class HHVacancy(Vacancy, CountMixin):  # add counter mixin
    """ HeadHunter Vacancy """

    def get_count_of_vacancy(self):
        pass

    def __str__(self):
        return f'\nHH: {self.name}, зарплата {self.salary},\nОписание: {self.discription},\nСсылка: {self.url}\nгород: {self.city}\n'


class SJVacancy(Vacancy, CountMixin):  # add counter mixin
    """ SuperJob Vacancy """

    def get_count_of_vacancy(self):
        pass

    def __str__(self):
        return f'\nSJ: {self.name}, зарплата {self.salary},\nОписание: {self.discription},\nСсылка: {self.url}\nгород: {self.city}\n'
