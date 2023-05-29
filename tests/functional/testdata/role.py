from faker import Faker

from tests.functional.utils.helpers import ApiResponse

fake = Faker()


def get_role_data() -> dict:
    role_data = {
        "id": fake.uuid4(),
        "name": fake.name()
    }

    return role_data


def get_role_id_by_name(resp: ApiResponse, name: str) -> int:
    for role in resp.body:
        if role['name'] == name:

            return role['id']
