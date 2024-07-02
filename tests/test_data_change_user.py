import requests
from data_faker import get_sign_up_data
import allure

class TestDataChangeUser:
    @allure.title("Проверка изменения данных авторизованного пользователя")
    def test_update_user_data_with_authorization(self, data_change_user_url, add_user_url, delete_user_url):
        name, email, password = get_sign_up_data()
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(add_user_url, json=payload)
        response_data = response.json()
        access_token = response_data["accessToken"]
        headers = {
            "Authorization": access_token
        }
        updated_name = "Testname"
        payload = {"name": updated_name}
        response = requests.patch(data_change_user_url, json=payload,
                                  headers=headers)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["name"] == updated_name
        access_token = response_data["accessToken"]
        headers = {
            "Authorization": access_token
        }
        requests.delete(delete_user_url, headers=headers)

    @allure.title("Проверка изменения данных не авторизованного пользователя")
    def test_update_user_data_without_authorization(self, data_change_user_url):
        headers = {}
        updated_name = "Testname"
        payload = {"name": updated_name}
        response = requests.patch(data_change_user_url, json=payload,
                                  headers=headers)
        assert response.status_code == 401
        assert response.json()["success"] == False
        assert response.json()["message"] == "You should be authorised"