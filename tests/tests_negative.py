import allure
import requests as r
from conftest import bearer_token
from enums.enum_test_data import Handlers
from enums.enum_test_data import UserDataLiza as UserLiza, UserDataMichal as UserMichal

user_michal = {"first_name": UserMichal.first_name.value,
               "last_name": UserMichal.last_name.value,
               "email": UserMichal.email.value,
               "password": UserMichal.password.value}
user_liza = {"first_name": UserLiza.first_name.value,
             "last_name": UserLiza.last_name.value,
             "email": UserLiza.email.value.replace("@", ""),
             "password": UserLiza.password.value,
             "phone": UserLiza.phone.value}


@allure.suite("Negative Tests")
class TestsNegative:

    @allure.title("Test create user without 'phone' field")
    def test_create_user_wo_phone_field(self, bearer_token):
        """
        Method tests creating new user without field 'phone'
        Valid Body, field 'phone' missing
        Expected result: Status Code 422,
                         Error message contains info about missing field
        """
        response = r.post(url=f"{Handlers.base_url.value}{Handlers.create_user.value}",
                          headers={"Authorization": "Bearer " + bearer_token},
                          json=user_michal)
        assert response.status_code == 422, f"Response status code-{response.status_code}"
        assert "missing" and ["body", "phone"] in response.json()["detail"][0].values(), \
            "Error message difference from expected"


    @allure.title("Test create user with invalid 'email' field")
    def test_create_user_with_invalid_email(self, bearer_token):
        """
        Method tests creating new user with invalid 'email' field
        Valid body, field 'email' without '@'
        Expected result: Status code 422,
                         Error message contains info about invalid field
        """
        response = r.post(url=f"{Handlers.base_url.value}{Handlers.create_user.value}",
                          headers={"Authorization": "Bearer " + bearer_token},
                          json=user_liza)
        error_message = response.json()["detail"][0]
        assert response.status_code == 422, f"Response status code-{response.status_code}"
        assert "value_error" and ["body", "email"] in error_message.values(), \
            "Error message difference from expected"


    @allure.title("Test get user by non-existent email")
    def test_get_user_by_non_existent_email(self, bearer_token):
        """
        Method tests getting user by non-existent email
        Params: 'email'='not.existent@email'
        Expected result: Status code 404,
                         Error message contains 'not.existent@email not found'
        """
        response = r.get(
            url=f"{Handlers.base_url.value}{Handlers.get_user_by_email.value}",
            headers={"Authorization": "Bearer " + bearer_token},
            params={"email": user_liza["email"]})
        assert response.status_code == 404, f"Response status code-{response.status_code}"
        assert f"User {user_liza["email"]} not found" in response.json()["detail"], \
            "Error message difference from expected"


    @allure.title("Test get user by invalid query")
    def test_get_user_by_invalid_query(self, bearer_token):
        """

        Method tests getting user by id (undefined query parameter)
        Params: 'id' = existent_id
        Expected result: Status code 422,
                         Error message contains info about invalid query
        """
        response = r.get(
            url=f"{Handlers.base_url.value}{Handlers.get_user_by_email.value}",
            headers={"Authorization": "Bearer " + bearer_token},
            params={"phone": user_liza["phone"]})
        error_message = response.json()["detail"][0]
        assert response.status_code == 422, f"Response status code-{response.status_code}"
        assert "missing" and ["query", "email"] in error_message.values(), \
            "Error message difference from expected"


    @allure.title("Test delete user")
    def test_delete_user_for_tests(self, bearer_token):
        """
        Method tests delete user by email (not allowed method)
        Params: 'email' = existent_email
        Expected result: Status code 405,
                         Error message contains info about not allowed method
        """
        response = r.delete(
            url=f"{Handlers.base_url.value}{Handlers.get_user_by_email.value}",
            headers={"Authorization": "Bearer " + bearer_token},
            params={"email": user_liza["email"]})
        assert response.status_code == 405, f"Response status code-{response.status_code}"
        assert response.json()["detail"] == "Method Not Allowed", \
            "Error message difference from expected"
