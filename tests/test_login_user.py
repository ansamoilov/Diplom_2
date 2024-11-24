import pytest
import allure
from methods.user_methods import login_user
from data import MESSAGES


class TestUserLogin:

    @allure.title("Тест на логин с существующим пользователем")
    @allure.description("Проверяет успешный логин под существующим пользователем.")
    def test_login_existing_user(self, user_data):
        user_data, token = user_data
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        response = login_user(login_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data["success"] is True

    @pytest.mark.parametrize(
        "is_valid_email, is_valid_password, expected_message",
        [
            (False, True, MESSAGES["invalid_credentials"]),
            (True, False, MESSAGES["invalid_credentials"]),
            (False, False, MESSAGES["invalid_credentials"])
        ]
    )
    @allure.title("Тест на логин с неверным логином и паролем")
    @allure.description("Проверяет неуспешный логин с неверным логином или паролем.")
    def test_login_with_invalid_credentials(self, user_data, is_valid_email, is_valid_password, expected_message):
        user_data, _ = user_data
        email = user_data["email"] if is_valid_email else "invalid_email@test.com"
        password = user_data["password"] if is_valid_password else "invalid_password"
        login_data = {"email": email, "password": password}

        response = login_user(login_data)
        response_data = response.json()
        assert (response.status_code == 401 and response_data["success"] is False and
                response_data["message"] == expected_message)
