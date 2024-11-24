import requests
from data import REGISTER_USER_URL, DELETE_USER_URL, LOGIN_USER_URL, USER_INFO_URL, UPDATE_USER_URL
from faker import Faker

faker = Faker()


def create_user_credentials():
    """
    Генерирует уникальные данные пользователя для регистрации
    :return: словарь с email, password и name
    """
    return {
        "email": faker.email(),
        "password": faker.password(),
        "name": faker.first_name()
    }


def register_user(user_data):
    """
    Метод для регистрации пользователя. Возвращает ответ от сервера
    """
    response = requests.post(REGISTER_USER_URL, json=user_data)
    return response


def delete_user(token: str):
    """
    Метод для удаления пользователя, используя авторизационный токен
    :param token: Авторизационный токен пользователя
    :return: Ответ от сервера
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(DELETE_USER_URL, headers=headers)
    return response


def login_user(login_data):
    """
    Метод для логина пользователя.

    login_data: словарь с данными для авторизации:
    {
        "email": "user@example.com",
        "password": "password123"
    }

    Возвращает ответ от сервера.
    """
    response = requests.post(LOGIN_USER_URL, json=login_data)
    return response


def get_user_data(token):
    """
    Отправляет запрос на получение данных пользователя

    :param token: Токен авторизации пользователя
    :return: Объект ответа (Response)
    """
    headers = {"Authorization": token}
    response = requests.get(USER_INFO_URL, headers=headers)
    return response


def update_user_data(token, update_data):
    """
    Отправляет запрос на обновление данных пользователя

    :param token: Токен авторизации пользователя
    :param update_data: Словарь с данными для обновления
                        Пример: {"email": "new_email@example.com"}
    :return: Объект ответа (Response), содержащий статус и результат обновления
    """
    headers = {"Authorization": token}
    response = requests.patch(UPDATE_USER_URL, json=update_data, headers=headers)
    return response



