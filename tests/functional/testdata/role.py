from faker import Faker

from tests.functional.utils.helpers import make_get_request
from tests.functional.utils.routes import ROLES_URL

fake = Faker()


def get_role_data() -> dict:
    role_data = {
        "id": fake.uuid4(),
        "name": fake.name()
    }

    return role_data


def get_role_id_by_name(name: str, access_token: str) -> int:
    resp = make_get_request(ROLES_URL, token=access_token)
    for role in resp.body:
        if role['name'] == name:

            return role['id']
