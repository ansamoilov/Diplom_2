#urls
BASE_URL = "https://stellarburgers.nomoreparties.site/api/"

REGISTER_USER_URL = f"{BASE_URL}auth/register"
DELETE_USER_URL = f"{BASE_URL}auth/user"
LOGIN_USER_URL = f"{BASE_URL}auth/login"
USER_INFO_URL = f"{BASE_URL}auth/user"
UPDATE_USER_URL = f"{BASE_URL}auth/user"
INGREDIENTS_URL = f"{BASE_URL}ingredients"
ORDERS_URL = f"{BASE_URL}orders"

#messages
MESSAGES = {
    "user_exists": "User already exists",
    "missing_fields": "Email, password and name are required fields",
    "invalid_credentials": "email or password are incorrect",
    "unauthorized": "You should be authorised",
    "ingredient_ids_required": "Ingredient ids must be provided"
}
