from tests.functional.settings import test_settings

BASE_URL = f'http://{test_settings.host_api}:{test_settings.port_api}/api/v1'

ADMIN_USER_URL = f'{BASE_URL}/admin/users'
AUTH_URL = f'{BASE_URL}/auth'
ROLES_URL = f'{BASE_URL}/admin/roles'

AUTH_URL_LOGIN = f'{AUTH_URL}/login'
AUTH_URL_SIGN_UP = f'{AUTH_URL}/sign_up'
