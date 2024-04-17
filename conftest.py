import pytest
import requests


@pytest.fixture(scope="function")
def bearer_token():
    response = requests.post("http://194.79.44.70:9090/api/v1/auth/login",
                             data={"username": "p.bodak@quality-lab.ru",
                                   "password": "gNiExb<S3!9x"})
    return response.json()['access_token']
