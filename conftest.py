import  pytest
import allure
from data import add_user_url, delete_user_url, login_user_url, ingredients_url
import requests
from data_faker import get_sign_up_data

@allure.step("регистрация пользователя")
@pytest.fixture(scope="module")
def user_data():
    name, email, password = get_sign_up_data()
    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    requests.post(add_user_url, json=payload)
    yield email, password
    login_response = requests.post(login_user_url, json={"email": email, "password": password})
    login_data = login_response.json()
    access_token = login_data["accessToken"]
    headers = {"Authorization": access_token}
    requests.delete(delete_user_url, headers=headers)

@allure.step("получение токена")
@pytest.fixture
def user_token(user_data):
    email, password = user_data
    payload = {
        "email": email,
        "password": password
    }
    login_response = requests.post(login_user_url, json=payload)
    login_data = login_response.json()
    access_token = login_data["accessToken"]
    yield access_token

@allure.step("получение ингридиентов")
@pytest.fixture
def ingredients():
    ingredients_response = requests.get(ingredients_url)
    ingredients_data = ingredients_response.json()
    return ingredients_data['data']