import allure

from helpers import register_new_user, create_user_data, send_post_request
from endpoints import Endpoints
from data import INCORRECT_EMAIL_OR_PASSWORD_MESSAGE


class TestLoginUser:
    @allure.title('Авторизация под существующим пользователем')
    def test_login_with_existing_user(self, delete_user_after_test):
        user_data = create_user_data()
        new_user_data = register_new_user(user_data)
        delete_user_after_test.append(new_user_data)
        login_data = {
            'email': user_data['email'],
            'password': user_data['password'],
        }

        response = send_post_request(Endpoints.URL + Endpoints.AUTH, login_data, 'Авторизация')

        assert response.status_code == 200 and 'accessToken' in response.json()

    @allure.title('Вход с неверным логином и паролем')
    def test_login_with_wrong_login_and_password(self):
        user_data = create_user_data()
        login_data = {
            'email': user_data['email'],
            'password': user_data['password'],
        }

        response = send_post_request(Endpoints.URL + Endpoints.AUTH, login_data, 'Авторизация')

        assert response.status_code == 401 and response.json().get('message') == INCORRECT_EMAIL_OR_PASSWORD_MESSAGE
