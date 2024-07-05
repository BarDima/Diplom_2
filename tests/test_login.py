import requests
from data_faker import get_sign_up_data
import allure
from data import add_user_url, delete_user_url, login_user_url

class TestLogin:
    @allure.title("Проверка авторизации существующего пользователя")
    def test_login(self):
        name, email, password = get_sign_up_data()
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        requests.post(add_user_url, json=payload)

        payload = {
            "email": email,
            "password": password
        }
        login_response = requests.post(login_user_url, json=payload)
        assert login_response.status_code == 200
        response_data = login_response.json()

        access_token = response_data["accessToken"]
        headers = {
            "Authorization": access_token
        }
        requests.delete(delete_user_url, headers=headers)

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


