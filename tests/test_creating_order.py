import requests

import allure
from data import creating_order_url


class TestCreatingOrder:

    @allure.title("Проверка создания заказа авторизованным пользователем")
    def test_creating_order_with_authorization(self, user_token, ingredients):
        ingredient1_id = ingredients[2]["_id"]
        ingredient2_id = ingredients[3]["_id"]
        order_payload = {
            "ingredients": [ingredient1_id, ingredient2_id]
        }
        headers = {
            "Authorization": user_token
        }
        order_response = requests.post(creating_order_url, json=order_payload, headers=headers)
        assert order_response.status_code == 200
        assert order_response.json()["success"] is True

    @allure.title("Проверка создания заказа не авторизованным пользователем")
    def test_creating_order_without_authorization(self, ingredients):
        ingredient1_id = ingredients[2]["_id"]
        ingredient2_id = ingredients[3]["_id"]
        order_payload = {
            "ingredients": [ingredient1_id, ingredient2_id]
        }
        order_response = requests.post(creating_order_url, json=order_payload)
        assert order_response.status_code == 200

    @allure.title("Проверка создания заказа с неверным хэшем ингредиентов")
    def test_creating_order_with_invalid_ingredient_id(self, user_token):
        order_payload = {
            "ingredients": ["61c0c5a71d1f82001bda70", "61c0c5a71d1f82001aa72"]
        }

        headers = {
            "Authorization": user_token
        }

        order_response = requests.post(creating_order_url, json=order_payload, headers=headers)
        assert order_response.status_code == 500

    @allure.title("Проверка создания заказа без ингредиентов")
    def test_creating_order_without_ingredient_id(self, user_token):
        order_payload = {
            "ingredients": []
        }

        headers = {
            "Authorization": user_token
        }

        order_response = requests.post(creating_order_url, json=order_payload, headers=headers)
        assert order_response.status_code == 400
        response_data = order_response.json()
        expected_message = "Ingredient ids must be provided"
        assert response_data["success"] is False
        assert response_data["message"] == expected_message


