def get_name_hh(data):
    name = data['name']

    return name


def get_url_hh(data):
    url = data['alternate_url']

    return url


def get_discription_hh(data):
    if data['snippet']['responsibility'] is None:
        return 'Нет описания'
    else:
        discription = data['snippet']['responsibility']
    return discription


def get_salary_hh(data):
    if data['salary'] is None:
        return 'Договорная'
    if data['salary']['from'] is None:
        return f"до {data['salary']['to']}"
    else:
       salary = f"от {data['salary']['from']} до {data['salary']['to']} руб/месяц"
    return salary


def get_city_hh(data):

    city = data['area']['name']

    return city

def get_name_sj(data):
    name = list(data).get('objects')[0].get('profession')
    return name


def get_url_sj(data):
    url = data.get('objects')[0].get('link')
    return url


def get_discription_sj(data):
    discription = data.get('objects')[0].get('candidat').replace('\n', '').replace('•', '')
    return discription


def get_salary_sj(data):
    salary = f"{data.get('objects')[0].get('payment_from')} до {data.get('objects')[0].get('payment_to')}"
    return salary


def get_city_sj(data):
    city = data.get('objects')[0].get('address')
    return city