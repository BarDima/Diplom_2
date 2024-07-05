import allure
import requests
from data import creating_order_url, receiving_order_url

class TestReceivingOrder:
    @allure.title("Проверка получения заказов авторизованного пользователя")
    def test_receiving_order_with_authorization(self, user_token, ingredients):
        ingredient1_id = ingredients[2]["_id"]
        ingredient2_id = ingredients[3]["_id"]
        order_payload = {
            "ingredients": [ingredient1_id, ingredient2_id]
        }

        headers = {
            "Authorization": user_token
        }
        requests.post(creating_order_url, json=order_payload, headers=headers)
        get_orders_response = requests.get(receiving_order_url, headers=headers)
        assert get_orders_response.status_code == 200
        orders_data = get_orders_response.json()
        assert orders_data["success"] is True

    @allure.title("Проверка получения заказов не авторизованного пользователя")
    def test_receiving_order_without_authorization(self):
        receiving_order_response = requests.get(receiving_order_url)
        assert receiving_order_response.status_code == 401
        response_data = receiving_order_response.json()
        expected_message = "You should be authorised"
        assert response_data["message"] == expected_message