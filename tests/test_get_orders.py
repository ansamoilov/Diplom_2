import allure
from methods.order_methods import get_user_orders, get_ingredients, create_order
from data import ORDERS_URL, MESSAGES


class TestGetOrders:
    @allure.title("Получение заказов авторизованным пользователем")
    @allure.description("Проверяет, что авторизованный пользователь может получить список своих заказов.")
    def test_get_orders_with_authorization(self, user_data):
        _, token = user_data
        ingredients_response = get_ingredients()
        ingredients_data = ingredients_response.json()
        ingredient_ids = [item["_id"] for item in ingredients_data["data"][:2]]
        first_order_response = create_order(ORDERS_URL, ingredient_ids, token)
        first_order_data = first_order_response.json()
        second_order_response = create_order(ORDERS_URL, ingredient_ids, token)
        second_order_data = second_order_response.json()
        response = get_user_orders(ORDERS_URL, token)
        response_data = response.json()
        order_numbers = [order["number"] for order in response_data["orders"]]
        assert (response.status_code == 200 and response_data["success"] is True
                and first_order_data["order"]["number"] in order_numbers
                and second_order_data["order"]["number"] in order_numbers)

    @allure.title("Получение заказов неавторизованным пользователем")
    @allure.description("Проверяет, что неавторизованный пользователь не может получить список заказов.")
    def test_get_orders_without_authorization(self):
        response = get_user_orders(ORDERS_URL, None)
        response_data = response.json()
        assert (response.status_code == 401 and response_data["success"] is False
                and response_data["message"] == MESSAGES["unauthorized"])
