import requests
from data import INGREDIENTS_URL


def get_ingredients():
    """
    Отправляет запрос на получение списка ингредиентов
    Возвращает объект ответа
    """
    response = requests.get(INGREDIENTS_URL)
    return response


def create_order(url, ingredients, token=None):
    """
    Отправляет запрос на создание заказа.

    :param url: URL для создания заказа
    :param ingredients: список идентификаторов ингредиентов
    :param token: токен авторизации (опционально)
    :return: объект ответа
    """
    headers = {}
    if token:
        headers["Authorization"] = token
    payload = {"ingredients": ingredients}
    response = requests.post(url, json=payload, headers=headers)
    return response


def get_user_orders(url, token):
    """
    Отправляет запрос на получение списка заказов пользователя

    :param url: URL для получения заказов
    :param token: Токен авторизации пользователя (опционально)
    :return: Объект ответа (Response)
    """
    headers = {"Authorization": f"{token}"} if token else {}
    response = requests.get(url, headers=headers)
    return response
