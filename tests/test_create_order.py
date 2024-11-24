import pytest
import allure
from methods.order_methods import create_order
from data import ORDERS_URL, MESSAGES


@allure.suite("Тесты на создание заказов")
class TestOrderCreation:
    @allure.title("Создание заказа с авторизацией")
    @allure.description("Проверяет успешное создание заказа, если пользователь авторизован.")
    def test_create_order_with_authorization(self, user_data, base_ingredients):
        _, token = user_data
        ingredients = base_ingredients[:2]
        response = create_order(ORDERS_URL, ingredients, token)
        response_data = response.json()
        assert (response.status_code == 200 and response_data["success"] is True
                and "order" in response_data and "number" in response_data["order"])

    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверяет успешное создание заказа, если пользователь не авторизован.")
    def test_create_order_without_authorization(self, base_ingredients):
        ingredients = base_ingredients[:2]
        response = create_order(ORDERS_URL, ingredients)
        response_data = response.json()
        assert (response.status_code == 200 and response_data["success"] is True
                and "order" in response_data and "number" in response_data["order"])

    @pytest.mark.parametrize(
        "token, expected_status, expected_success, expected_message",
        [
            (None, 400, False, MESSAGES["ingredient_ids_required"]),
            ("valid_token", 400, False, MESSAGES["ingredient_ids_required"]),
        ]
    )
    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Проверяет, что заказ не может быть создан без ингредиентов.")
    def test_create_order_without_ingredients(self, user_data, token, expected_status, expected_success,
                                              expected_message):
        if token == "valid_token":
            _, token = user_data
        else:
            token = None
        ingredients = []
        response = create_order(ORDERS_URL, ingredients, token)
        response_data = response.json()
        assert (response.status_code == expected_status and
                response_data["success"] is expected_success and
                response_data["message"] == expected_message)

    @pytest.mark.parametrize(
        "token, ingredients, expected_status",
        [
            (None, ["invalid_hash_1", "invalid_hash_2"], 500),
            ("valid_token", ["invalid_hash_1", "invalid_hash_2"], 500),
        ]
    )
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.description("Проверяет, что заказ не может быть создан с невалидными ингредиентами.")
    def test_create_order_with_invalid_ingredients_hash(self, user_data, token, ingredients, expected_status):
        if token == "valid_token":
            _, token = user_data
        else:
            token = None
        response = create_order(ORDERS_URL, ingredients, token)
        assert response.status_code == expected_status
