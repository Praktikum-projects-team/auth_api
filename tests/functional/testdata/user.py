from faker import Faker

from tests.functional.utils.constants import UserData

fake = Faker()


def get_user_sign_up_data() -> dict:
    user_data = {
        "name": fake.name(),
        "login": UserData.LOGIN,
        "password": UserData.PASSWORD
    }
    return user_data


def get_user_login_data() -> dict:
    user_data = {
        "login": UserData.LOGIN,
        "password": UserData.PASSWORD
    }
    return user_data
