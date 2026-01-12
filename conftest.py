import pytest

from helpers import delete_user


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
