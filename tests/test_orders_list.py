import requests
import allure
import pytest
from urls import Urls


class TestOrdersListGet:

    @allure.title('Проверка получения списка заказов')
    @allure.description('Проверяются код и тело ответа.')
    def test_orders_list_get_success(self):
        response = requests.get(Urls.URL_orders_create)
        assert response.status_code == 200
        data = response.json()
        assert 'orders' in data and isinstance(data['orders'], list)
        if len(data['orders']) > 0:
            assert 'id' in data['orders'][0]