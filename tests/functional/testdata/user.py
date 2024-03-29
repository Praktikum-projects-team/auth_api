from faker import Faker

fake = Faker()


def get_user_data() -> dict:
    user_data = {
        "id": fake.uuid4(),
        "login": fake.email(),
        "password": fake.password(),
        "name": fake.name()
    }

    return user_data
