import pytest
import allure

@allure.step("Возвращение URL запроса создание пользователя")
@pytest.fixture
def add_user_url():
    return "https://stellarburgers.nomoreparties.site/api/auth/register"

@allure.step("Возвращение URL запроса удаление пользователя")
@pytest.fixture
def delete_user_url():
    return "https://stellarburgers.nomoreparties.site/api/auth/user"

@allure.step("Возвращение URL запроса авторизации пользователя")
@pytest.fixture
def login_user_url():
    return "https://stellarburgers.nomoreparties.site/api/auth/login"

@allure.step("Возвращение URL запроса изменение данных пользователя")
@pytest.fixture
def data_change_user_url():
    return "https://stellarburgers.nomoreparties.site/api/auth/user"

@allure.step("Возвращение URL запроса получения ингредиентов")
@pytest.fixture
def ingredients_url():
    return "https://stellarburgers.nomoreparties.site/api/ingredients"

@allure.step("Возвращение URL запроса создание заказа")
@pytest.fixture
def creating_order_url():
    return "https://stellarburgers.nomoreparties.site/api/orders"

@allure.step("Возвращение URL запроса получение списка заказов")
@pytest.fixture
def receiving_order_url():
    return " https://stellarburgers.nomoreparties.site/api/orders"



