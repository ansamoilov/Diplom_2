import pytest

from methods.order_methods import get_ingredients
from methods.user_methods import create_user_credentials, register_user, delete_user


@pytest.fixture
def user_data():
    """
    Фикстура для создания данных пользователя
    Генерирует уникальные данные для каждого теста и удаляет пользователя после теста
    """
    user_data = create_user_credentials()
    response = register_user(user_data)
    response_data = response.json()
    token = response_data.get("accessToken")
    yield user_data, token
    delete_user(token)


@pytest.fixture(scope="session")
def base_ingredients():
    """
    Фикстура для получения списка ингредиентов
    Выполняется один раз за сессию
    """
    response = get_ingredients()
    assert response.status_code == 200
    return [ingredient["_id"] for ingredient in response.json()["data"]]
