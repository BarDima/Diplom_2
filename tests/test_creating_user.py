import requests
from data_faker import get_sign_up_data
import allure
from data import add_user_url, delete_user_url

class TestCreateUser:
    @allure.title("Проверка создания пользователя")
    def test_create_user(self):
        name, email, password = get_sign_up_data()

        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(add_user_url, json=payload)
        assert response.status_code == 200
        response_data = response.json()

        access_token = response_data["accessToken"]
        headers = {
            "Authorization": access_token
        }
        delete_response = requests.delete(delete_user_url, headers=headers)
        assert delete_response.status_code == 202

    @allure.title("Проверка создания пользователя, который уже зарегистрирован")
    def test_create_existing_user(self):
        payload = {
            "email": "test-data@yandex.ru",
            "password": "password",
            "name": "Username"
        }
        response = requests.post(add_user_url, json=payload)
        assert response.status_code == 403
        assert "User already exists" in response.json()["message"]

    @allure.title("Проверка создания пользователя, без заполнения обязательного поля password")
    def test_create_user_missing_fields(self):
        payload = {
            "email": "test-data@yandex.ru"
        }
        response = requests.post(add_user_url, json=payload)
        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.json()["message"]
