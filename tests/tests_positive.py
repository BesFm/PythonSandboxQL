import pytest
import requests as r
from enums.enum_test_data import Handlers
from enums.enum_test_data import UserDataLiza as UserLiza, UserDataMichal as UserMichal
from conftest import bearer_token

user_data_liza = {"first_name": UserLiza.first_name.value,
                  "last_name": UserLiza.last_name.value,
                  "email": UserLiza.email.value,
                  "password": UserLiza.password.value,
                  "phone": UserLiza.phone.value}
user_data_michal = {"first_name": UserMichal.first_name.value,
                    "last_name": UserMichal.last_name.value,
                    "email": UserMichal.email.value,
                    "password": UserMichal.password.value,
                    "phone": ""}  # тест get user by email падает при пустом phone


class TestsPositive:

    def test_get_all_users(self, bearer_token):
        """
        Method tests getting all users
        Expected result: Status code 200, response body contains users
        """
        response = r.get(url=f"{Handlers.base_url.value}{Handlers.get_users.value}",
                         headers={"Authorization": "Bearer " + bearer_token})
        assert response.status_code == 200, f"Response status code-{response.status_code}"
        assert len(response.json()) > 1, "Response content is empty"


    @pytest.mark.parametrize("user_data",
                             [user_data_liza,
                              pytest.param(user_data_michal, marks=pytest.mark.xfail)])
    def test_create_user(self, bearer_token, user_data):
        """
        Method tests creating user
        Expected result: Status code 201, response body contains created user
        """
        response = r.post(url=f"{Handlers.base_url.value}{Handlers.create_user.value}",
                          headers={"Authorization": "Bearer " + bearer_token},
                          json=user_data)
        response_body = [field for field in response.json().values()]
        request_body = [field for field in user_data.values()]
        assert response.status_code == 201, f"Response status code-{response.status_code}"
        assert response_body[:-1] == request_body, \
            "Response body difference from expected"


    @pytest.mark.parametrize("email, user_data",
                             [(UserLiza.email.value, user_data_liza),
                              (UserMichal.email.value, user_data_michal)])
    def test_get_user_by_email(self, bearer_token, email, user_data):
        """
        Method tests getting user by email param
        Expected result: Status code 200, Response body contains user, with suitable email
        """

        response = r.get(
            url=f"{Handlers.base_url.value}{Handlers.get_user_by_email.value}",
            params={"email": email},
            headers={"Authorization": "Bearer " + bearer_token})
        assert response.status_code == 200, "Response status code-{response.status_code}"
        assert user_data == response.json(), "Response body difference from expected"
