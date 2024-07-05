from faker import Faker
import allure

@allure.step("Генерируем случайное имя, почту, пароль")
def get_sign_up_data():
    fake = Faker()
    name = fake.name()
    email = fake.email()
    password = fake.password()
    return name, email, password



