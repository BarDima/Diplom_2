import requests
from data_faker import get_sign_up_data
import allure
from data import add_user_url, delete_user_url, login_user_url, ingredients_url, creating_order_url, receiving_order_url, data_change_user_url


class TestCreatingOrder:

    @allure.title("Проверка создания заказа авторизованным пользователем")
    def test_creating_order_with_authorization(self):
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
        login_data = login_response.json()
        access_token = login_data["accessToken"]
        ingredients_response = requests.get(ingredients_url)
        ingredients_data = ingredients_response.json()
        ingredients_list = ingredients_data['data']
        ingredient1_id = ingredients_list[2]["_id"]
        ingredient2_id = ingredients_list[3]["_id"]
        ingredients = [ingredient1_id, ingredient2_id]

        order_payload = {
            "ingredients": ingredients
        }

        headers = {
            "Authorization": access_token
        }

        order_response = requests.post(creating_order_url, json=order_payload, headers=headers)
        assert order_response.status_code == 200
        requests.delete(delete_user_url, headers=headers)

    @allure.title("Проверка создания заказа не авторизованным пользователем")
    def test_creating_order_without_authorization(self):
        ingredients_response = requests.get(ingredients_url)
        ingredients_data = ingredients_response.json()
        ingredients_list = ingredients_data['data']
        ingredient1_id = ingredients_list[2]["_id"]
        ingredient2_id = ingredients_list[3]["_id"]
        ingredients = [ingredient1_id, ingredient2_id]

        order_payload = {
            "ingredients": ingredients
        }
        order_response = requests.post(creating_order_url, json=order_payload)
        assert order_response.status_code == 200

    @allure.title("Проверка создания заказа с неверным хэшем ингредиентов")
    def test_creating_order_with_invalid_ingredient_id(self):
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
        login_data = login_response.json()
        access_token = login_data["accessToken"]
        order_payload = {
            "ingredients": ["61c0c5a71d1f82001bda70","61c0c5a71d1f82001aa72"]
        }

        headers = {
            "Authorization": access_token
        }

        order_response = requests.post(creating_order_url, json=order_payload, headers=headers)
        assert order_response.status_code == 500
        requests.delete(delete_user_url, headers=headers)

    @allure.title("Проверка создания заказа без ингредиентов")
    def test_creating_order_without_ingredient_id(self):
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
        login_data = login_response.json()
        access_token = login_data["accessToken"]
        order_payload = {
            "ingredients": []
        }

        headers = {
            "Authorization": access_token
        }

        order_response = requests.post(creating_order_url, json=order_payload, headers=headers)
        assert order_response.status_code == 400
        response_data = order_response.json()
        expected_message = "Ingredient ids must be provided"
        assert response_data["success"] is False
        assert response_data["message"] == expected_message
        requests.delete(delete_user_url, headers=headers)


