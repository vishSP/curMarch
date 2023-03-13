from abc import ABC, abstractmethod

import requests

from utils import *


class Engine(ABC):

    @abstractmethod
    def get_request(self, url: str, params: dict, headers=None):

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
        return super().get_request(url=self.__url, params=self.__params).json()


    def get_formatted_data(self,unformatted_data):

        about_vacancy = {
            'site_name': 'HH.ru',
            'name': get_name_hh(unformatted_data),
            'url': get_url_hh(unformatted_data),
            'discription': get_discription_hh(unformatted_data),
            'salary': get_salary_hh(unformatted_data),
            'city': get_city_hh(unformatted_data)

        }
        return about_vacancy


    def get_vacancy_lsit(self):

        vacancy_list = []
        page = 0
        print('Идет поиск вакансий...')
        while True:
            self.__params['pages'] = page
            data = self.get_request()
            for item in data.get('items'):

                vacancy_list.append(Vacancy(data=self.get_formatted_data(unformatted_data=item)))
            if data.get('pages') - page <= 1:
                print(f'\nВакансий найдено:{len(vacancy_list)}')
                break
            else:
                page += 1
        return vacancy_list


class Superjob(Engine):

    def __init__(self):
        self.my_auth_data = {
            'X-Api-App-Id': 'v3.r.137417367.c9eaf0a7d9ee18a7194f5c2b75fa46c86b533977.0146fbc82574c0cec8667869d1e560f196632d85'}
        self.__url = 'https://api.superjob.ru/2.0/vacancies'
        self.__params = {"keywords": 'python', "page": 2}

    def get_request(self):
        return super().get_request(url=self.__url, params=self.__params, headers=self.my_auth_data).json()

    def get_formatted_data(self):
        unformatted_data = self.get_request()

        about_vacancy = {
            'site_name': 'Superjob.ru',
            'name': get_name_sj(unformatted_data),
            'url': get_url_sj(unformatted_data),
            'discription': get_discription_sj(unformatted_data),
            'salary': get_salary_sj(unformatted_data),
            'city': get_city_sj(unformatted_data)

        }
        return about_vacancy


class Vacancy:
    __slots__ = ['data']

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f'\nHH: {self.name}, зарплата {self.salary},\nОписание: {self.discription},\nСсылка: {self.url}\nгород: {self.city}\n'
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


"выведи ссылку superjob"
hh = HH()

ss = Superjob()

print(hh.get_vacancy_lsit())
