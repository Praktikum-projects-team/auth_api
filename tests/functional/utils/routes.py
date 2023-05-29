from tests.functional.settings import test_settings

BASE_URL = f'http://{test_settings.host_api}:{test_settings.port_api}/api/v1'

AUTH_URL = f'{BASE_URL}/auth'
ROLES_URL = f'{BASE_URL}/admin/roles'
