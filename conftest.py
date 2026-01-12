import pytest

from helpers import delete_user, send_get_request, create_user_data, register_new_user
from endpoints import Endpoints


@pytest.fixture(scope='function')
def delete_user_after_test():
    users_data = []

    yield users_data

    for data in users_data:
        try:
            delete_user(data, data['email'])
            print(f'Удален пользователь с email: {data['email']}')
        except Exception as e:
            print(f'Ошибка удаления пользователя с email: {data['email']}: {e}')

@pytest.fixture(scope='class')
def ingredients_info():
    print('dada')
    response = send_get_request(Endpoints.URL + Endpoints.INGREDIENTS, 'Отправляем запрос на получение данных об ингредиентах')

    return response.json().get('data')

@pytest.fixture(scope='function')
def credentials():
    response = register_new_user(create_user_data())

    return {
        'accessToken': response['accessToken'],
        'email': response['email']
    }
