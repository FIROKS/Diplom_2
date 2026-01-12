import string
import random
import allure
import requests

from endpoints import Endpoints


@allure.step('{title}')
def send_post_request(url, data, title, token=None ):
    response = None
    if token:
        headers = {
            'Authorization': token
        }
        response = requests.post(url, data, headers=headers)
    else:
        response = requests.post(url, data)

    return response

@allure.step('{title}')
def send_get_request(url, title):
    return requests.get(url)

@allure.step('Удаляем пользователя с почтой {email}')
def delete_user(user_data, email):
    headers = {
        'Authorization': user_data['accessToken']
    }

    requests.delete(Endpoints.URL + Endpoints.DELETE_USER, headers=headers)

@allure.step('Регистрируем нового пользователя')
def register_new_user(payload):
    data = {}
    response = send_post_request(Endpoints.URL + Endpoints.CREATE_USER, payload, 'Отправляем запрос на создание нового пользователя')

    if response.status_code == 200:
        credentials = response.json()
        data['accessToken'] = credentials.get('accessToken')
    
    data['email'] = payload['email']
    data['name'] = payload['name']
    data['response'] = response
    return data

def generate_random_string():
    length = 10
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def generate_user_email():
    return f'{generate_random_string()}@mail.ru'

@allure.step('Создаем данные для нового пользователя')
def create_user_data():
    data = {
        'email': generate_user_email(),
        'password': generate_random_string(),
        'name': generate_random_string()
    }

    return data

def get_list_for_create_user_without_any_param():
    list = []
    # Заполняет массив комбинациями без какого-то одого параметра
    for i in range(3):
        data = create_user_data()
        match i:
             case 0:
                  list.append(('', data['password'], data['name']))
             case 1:
                  list.append((data['email'], '', data['name']))
             case 2:
                  list.append((data['email'], data['password'], ''))
    return list
