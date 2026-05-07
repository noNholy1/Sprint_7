import requests
import allure
import pytest
from data import Data
from urls import Urls
from helpers import create_random_login, create_random_password, create_random_firstname


class TestCourierLogin:

    @allure.title('Проверка успешной аутентификации курьера при вводе валидных данных')
    @allure.description('Happy path. Проверяются код и тело ответа.')
    def test_courier_login_success(self):
        with allure.step('Отправка запроса на авторизацию с валидными данными'):
            response = requests.post(Urls.URL_courier_login, json=Data.valid_courier_data)
        assert response.status_code == 200 and 'id' in response.text

    @allure.title('Проверка получения ошибки аутентификации курьера при вводе невалидных данных')
    @allure.description('В тест по очереди передаются наборы данных с несуществующим логином или неверным паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('nonexistent_credentials', [
        {'login': create_random_login(), 'password': create_random_password()},
        Data.courier_data_with_wrong_password
    ])
    def test_courier_login_nonexistent_data_not_found(self, nonexistent_credentials):
        with allure.step('Отправка запроса на авторизацию с невалидными данными'):
            response = requests.post(Urls.URL_courier_login, json=nonexistent_credentials)
        assert response.status_code == 404
        assert response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка получения ошибки аутентификации курьера с пустым полем логина или пароля')
    @allure.description('В тест по очереди передаются наборы данных с пустым логином или паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('missing_fields', [
        {'password': create_random_password()},
        {'login': '', 'password': create_random_password()},
        {'login': Data.valid_login, 'password': ''}
])
    def test_courier_login_missing_fields_bad_request(self, missing_fields):
        with allure.step('Отправка запроса на авторизацию с неполными данными'):
            response = requests.post(Urls.URL_courier_login, json=missing_fields)
        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для входа'