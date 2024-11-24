import pytest
import allure
from methods.user_methods import login_user, update_user_data, create_user_credentials, register_user, delete_user


class TestUserUpdate:
    @pytest.mark.parametrize(
        "update_data, expected_value",
        [
            ({"name": "Updated User Name"}, "Updated User Name"),
            ({"email": create_user_credentials()["email"]}, None)
        ]
    )
    @allure.title("Тест на изменение данных пользователя с авторизацией")
    @allure.description("Проверяет успешное изменение данных пользователя с авторизацией.")
    def test_update_user_data_with_authorization(self, user_data, update_data, expected_value):
        user_data, token = user_data
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        response = login_user(login_data)
        response_data = response.json()
        access_token = response_data.get("accessToken")
        response = update_user_data(access_token, update_data)
        response_data = response.json()
        updated_key = list(update_data.keys())[0]
        updated_value = response_data["user"].get(updated_key)
        assert (response.status_code == 200 and response_data["success"]
                and updated_value == (update_data.get(updated_key) if updated_key != "email"
                                      else update_data[updated_key]))

    @allure.title("Тест на изменение данных пользователя без авторизации")
    @allure.description("Проверяет попытку изменить данные пользователя без авторизации.")
    def test_update_user_data_without_authorization(self):
        update_data = {"name": "Updated User Name"}
        expected_message = "You should be authorised"
        response = update_user_data("", update_data)
        response_data = response.json()
        assert (response.status_code == 401 and response_data["success"] is False
                and response_data["message"] == expected_message)

    @allure.title("Тест на изменение почты на уже существующую с авторизацией")
    @allure.description("Проверяет попытку изменить email на уже существующий с авторизацией.")
    def test_update_email_with_existing_email_with_authorization(self, user_data):
        first_user_email = user_data[0]["email"]
        second_user_data = create_user_credentials()
        second_user_response = register_user(second_user_data)
        second_user_token = second_user_response.json().get("accessToken")
        update_data = {"email": first_user_email}
        response = update_user_data(second_user_token, update_data)
        response_data = response.json()
        assert (response.status_code == 403 and response_data["success"] is False and
                response_data["message"] == "User with such email already exists")
        delete_user(second_user_token)
