from faker import Faker

from tests.functional.utils.constants import UserData

fake = Faker()


def get_user_data() -> dict:
    user_data = {
        "id": fake.uuid4(),
        "login": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }

    return user_data


def get_user_sign_up_data() -> dict:
    user_data = {
        "id": fake.uuid4(),
        "name": fake.name(),
        "login": UserData.LOGIN,
        "password": UserData.PASSWORD
    }
    return user_data

