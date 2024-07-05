import allure
import requests
from data_faker import get_sign_up_data
from data import add_user_url, delete_user_url, login_user_url, ingredients_url, creating_order_url, receiving_order_url

class TestReceivingOrder:
    @allure.title("Проверка получения заказов авторизованного пользователя")
    def test_receiving_order_with_authorization(selfl):
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

        requests.post(creating_order_url, json=order_payload, headers=headers)

        headers = {
            "Authorization": access_token
        }
        create_order_response = requests.get(receiving_order_url, headers=headers)
        assert create_order_response.status_code == 200
        receiving_order_data = create_order_response.json()
        assert receiving_order_data["success"] is True
        requests.delete(delete_user_url, headers=headers)

    @allure.title("Проверка получения заказов не авторизованного пользователя")
    def test_receiving_order_without_authorization(self):
        receiving_order_response = requests.get(receiving_order_url)
        assert receiving_order_response.status_code == 401
        response_data = receiving_order_response.json()
        expected_message = "You should be authorised"
        assert response_data["message"] == expected_message