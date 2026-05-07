import requests
import allure
import pytest
from urls import Urls


class TestOrdersListGet:

    @allure.title('Проверка получения списка заказов')
    @allure.description('Проверяются код и тело ответа.')
    def test_orders_list_get_success(self):
        with allure.step('Отправка запроса на получение списка заказов'):
            response = requests.get(Urls.URL_orders_create)
        assert response.status_code == 200
        data = response.json()
        assert 'orders' in data and isinstance(data['orders'], list)
        assert all('id' in order for order in data['orders'])