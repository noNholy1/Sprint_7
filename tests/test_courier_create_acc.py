import requests
import allure
import pytest
from data import Data
from urls import Urls
from helpers import create_random_login, create_random_password, create_random_firstname


class TestCourierCreate:

    @allure.title('Проверка успешного создания аккаунта курьера с валидными данными')
    @allure.description('Happy path. Проверяются код и тело ответа.')
    def test_create_courier_account_success(self, delete_courier_after_test):
        payload = {
            'login': create_random_login(),
            'password': create_random_password(),
            'firstName': create_random_firstname()
        }
        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(Urls.URL_courier_create, json=payload)
        assert response.status_code == 201 and response.json() == {'ok': True}
        
        delete_courier_after_test['id'] = response.json().get('id')

    @allure.title('Проверка получения ошибки при повторном использовании логина для создания курьера')
    @allure.description('Проверяются код и тело ответа.')
    def test_create_courier_account_login_taken_conflict(self):
        payload = {
            'login': Data.valid_login,
            'password': create_random_password(),
            'firstName': create_random_firstname()
        }
        with allure.step('Отправка запроса на создание курьера с занятым логином'):
            response = requests.post(Urls.URL_courier_create, json=payload)
        assert response.status_code == 409
        assert response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Проверка получения ошибки при создании курьера с незаполненными обязательными полями')
    @allure.description('В тест по очереди передаются наборы данных с пустым логином или паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('incomplete_payload', [
        {'password': create_random_password(), 'firstName': create_random_firstname()},
        {'login': create_random_login(), 'firstName': create_random_firstname()}
])
    def test_create_courier_missing_required_fields(self, incomplete_payload):
        with allure.step('Отправка запроса на создание курьера с неполными данными'):
            response = requests.post(Urls.URL_courier_create, json=incomplete_payload)
        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для создания учетной записи'