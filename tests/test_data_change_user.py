import requests
import allure
from data import add_user_url, delete_user_url, data_change_user_url

class TestDataChangeUser:
    @allure.title("Проверка изменения данных авторизованного пользователя")
    def test_update_user_data_with_authorization(self, user_token):
        updated_name = "Testname"
        payload = {"name": updated_name}
        headers = {
            "Authorization": user_token
        }
        response = requests.patch(data_change_user_url, json=payload, headers=headers)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["name"] == updated_name

    @allure.title("Проверка изменения данных не авторизованного пользователя")
    def test_update_user_data_without_authorization(self):
        headers = {}
        updated_name = "Testname"
        payload = {"name": updated_name}
        response = requests.patch(data_change_user_url, json=payload,
                                  headers=headers)
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == "You should be authorised"