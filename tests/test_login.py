import requests
from data_faker import get_sign_up_data
import allure
from data import add_user_url, delete_user_url, login_user_url

class TestLogin:
    @allure.title("Проверка авторизации существующего пользователя")
    def test_login(self, user_data):
        email, password = user_data
        payload = {
            "email": email,
            "password": password
        }
        login_response = requests.post(login_user_url, json=payload)
        assert login_response.status_code == 200
        assert login_response.json()["success"] is True

    @allure.title("Проверка авторизации с неверным логином и паролем")
    def test_incorrect_login(self):
        payload = {
            "email": "email@yandex.ru",
            "password": "passwordd"
        }
        login_response = requests.post(login_user_url, json=payload)
        assert login_response.status_code == 401
        response_data = login_response.json()
        assert response_data.get("success") is False
        assert response_data.get(
            "message") == "email or password are incorrect"


