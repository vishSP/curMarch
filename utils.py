import json


def get_name_hh(data):
    """
    Ищет и возвращает имя вакансии

    """
    name = data['name']
    return name


def get_url_hh(data):
    """
    Ищет и возвращает ссылку вакансии

    """
    url = data['alternate_url']

    return url


def get_discription_hh(data):
    """
    Ищет и возвращает описание вакансии

    """
    if data['snippet']['responsibility'] is None:
        return 'Нет описания'
    else:
        discription = data['snippet']['responsibility']
    return discription


def get_salary_hh(data):
    """
    Ищет и возвращает зарпалату, либо ее отсутсвие

    """
    if data['salary'] is None:
        return 'Договорная'
    if data['salary']['from'] is None:
        return f"до {data['salary']['to']}"
    else:
        salary = f"от {data['salary']['from']} до {data['salary']['to']} руб/месяц"
    return salary


def get_city_hh(data):
    """
    Ищет и возвращает город

    """
    city = data['area']['name']

    return city


def get_name_sj(data):
    """
    Ищет и возвращает имя вакансии

    """
    name = data['profession']

    return name


def get_url_sj(data):
    """
    Ищет и возвращает ссылку вакансии

    """
    url = data['link']

    return url


def get_discription_sj(data):
    """
    Ищет и возвращает описание вакансии

    """
    discription = data['candidat'].replace('\n', '').replace('•', '')
    return discription


def get_salary_sj(data):
    if data["payment_from"] == 0 and data["payment_to"] == 0:
        return 'Договорная'
    if data["payment_from"] == 0:
        return f'до {data["payment_to"]} руб/месяц'
    if data['payment_to'] == 0:
        return f'{data["payment_from"]} руб/месяц'

    else:
        salary = f'{data["payment_from"]} до {data["payment_to"]} руб/месяц'
    return salary


def get_city_sj(data):
    """
    Ищет и возвращает город

    """
    if data['address'] is None:
        return data['town']['title']
    else:
        city = data['address']
    return city


def get_sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """

    sorted_salary = sorted(vacancies, key=lambda v: v.salary, reverse=True)
    return sorted_salary


def get_top(vacancies, top_count: int):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """

    sorted_salary = sorted(vacancies, key=lambda v: v.salary, reverse=True)[:top_count]
    return sorted_salary


def to_file(data: dict):
    """
    Записывает информацию в txt файл
    """
    my_file = open('vacancy.txt', 'w', encoding='utf8')
    for element in data:
        my_file.write((str(element)))
        my_file.write('\n')
    my_file.close()
