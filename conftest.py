import allure
import pytest
import requests as r
from enums.enum_test_data import Handlers


@pytest.fixture(scope="function")
def bearer_token():
    with allure.step("Get Bearer Token"):
        response = r.post(
            url=f"{Handlers.base_url.value}{Handlers.get_bearer_token.value}",
            data={"username": "p.bodak@quality-lab.ru",
                  "password": "gNiExb<S3!9x"})
    return response.json()['access_token']
