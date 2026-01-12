import allure
import pytest

from helpers import register_new_user, create_user_data, get_list_for_create_user_without_any_param
from data import EXISTING_USER_MESSAGE, REQUIRED_FIELDS_MESSAGE


class TestCreateUser:
    @allure.title('Успешное создание уникального пользователя')
    def test_create_unique_user(self, delete_user_after_test):
        user_data = create_user_data()
        new_user_data = register_new_user(user_data)
        delete_user_after_test.append(new_user_data)

        assert new_user_data['response'].status_code == 200

    @allure.title('Нельзя создать уже зарегистрированного пользователя')
    def test_create_existing_user(self, delete_user_after_test):
        user_data = create_user_data()
        
        new_user_data = register_new_user(user_data)
        existing_user = register_new_user(user_data)
        delete_user_after_test.append(new_user_data)
        delete_user_after_test.append(existing_user)
        
        assert existing_user['response'].status_code == 403 and existing_user['response'].json().get('message') == EXISTING_USER_MESSAGE

    @allure.title('Попытка создать пользователя с пустым обязательным полем')
    @pytest.mark.parametrize(
        'email, password, name', get_list_for_create_user_without_any_param()
    )
    def test_create_user_with_empty_param(self, email, password, name, delete_user_after_test):
        user_data = {
            'email': email,
            'password': password,
            'name': name
        }
        new_user_data = register_new_user(user_data)
        delete_user_after_test.append(new_user_data)

        assert new_user_data['response'].status_code == 403 and new_user_data['response'].json().get('message') == REQUIRED_FIELDS_MESSAGE
