import allure
import pytest

from methods.user_methods import register_user, create_user_credentials
from data import MESSAGES


class TestUserRegistration:

    @allure.title("Тест на регистрацию нового пользователя")
    @allure.description("Проверяет успешную регистрацию нового уникального пользователя.")
    def test_register_unique_user(self):
        user_data = create_user_credentials()
        response = register_user(user_data)
        response_data = response.json()
        assert response.status_code == 200 and response_data["success"] is True

    @allure.title("Тест на регистрацию существующего пользователя")
    @allure.description("Проверяет регистрацию пользователя, который уже существует.")
    def test_register_existing_user(self):
        user_data = create_user_credentials()
        register_user(user_data)
        response = register_user(user_data)
        response_data = response.json()
        assert (response.status_code == 403 and response_data["message"] == MESSAGES["user_exists"]
                and response_data["success"] is False)

    @allure.title("Тест на регистрацию с отсутствующим обязательным полем")
    @allure.description("Проверяет регистрацию пользователя с отсутствующим обязательным полем.")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_register_user_missing_field(self, missing_field):
        user_data = create_user_credentials()
        user_data.pop(missing_field)
        response = register_user(user_data)
        response_data = response.json()
        assert (response.status_code == 403 and response_data["message"] == MESSAGES["missing_fields"]
                and response_data["success"] is False)
