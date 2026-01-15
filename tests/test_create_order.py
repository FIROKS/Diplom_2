import allure

from helpers import send_post_request
from endpoints import Endpoints
from data import INGREDIENTS_NOT_PROVIDED


class TestCreateOrder:
    @allure.title('Создание заказа с авторизацией')
    def test_create_order_with_auth(self, credentials, ingredients_info, delete_user_after_test):
        ingredients = {
            'ingredients': [ingredients_info[0].get('_id')]
        }
        delete_user_after_test.append(credentials)

        response = send_post_request(Endpoints.URL + Endpoints.ORDER, ingredients, 'Создание заказа с авторизацией', credentials['accessToken'])

        assert response.status_code == 200 and 'number' in response.json().get('order')

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_auth(self, ingredients_info):
        ingredients = {
            'ingredients': [ingredients_info[0].get('_id')]
        }

        response = send_post_request(Endpoints.URL + Endpoints.ORDER, ingredients, 'Создание заказа без авторизацией')

        assert response.status_code == 401 and 'number' not in response.json().get('order')

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, credentials, delete_user_after_test):
        ingredients = {
            'ingredients': []
        }
        delete_user_after_test.append(credentials)

        response = send_post_request(Endpoints.URL + Endpoints.ORDER, ingredients, 'Создание заказа без ингредиентов', credentials['accessToken'])

        assert response.status_code == 400 and response.json().get('message') == INGREDIENTS_NOT_PROVIDED

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_wrong_hash(self, credentials, delete_user_after_test):
        ingredients = {
            'ingredients': ['ффффф']
        }
        delete_user_after_test.append(credentials)

        response = send_post_request(Endpoints.URL + Endpoints.ORDER, ingredients, 'Создание заказа с неверным хешем ингредиентов', credentials['accessToken'])

        assert response.status_code == 500
