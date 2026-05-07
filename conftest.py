import pytest
import requests
import allure
import pytest
from urls import Urls


@pytest.fixture
def delete_courier_after_test():
    courier_data = {}
    yield courier_data
    courier_id = courier_data.get('id')
    if courier_id:
        with allure.step(f'Удаление курьера с id={courier_id} после теста'):
            requests.delete(f"{Urls.URL_courier_create}/{courier_id}")