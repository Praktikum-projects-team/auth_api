from tests.functional.settings import test_settings

BASE_URL = f'http://{test_settings.host_api}:{test_settings.port_api}/api/v1'

ADMIN_USER_URL = f'{BASE_URL}/admin/users'
AUTH_URL = f'{BASE_URL}/auth'
ROLES_URL = f'{BASE_URL}/admin/roles'
USER_URL = f'{BASE_URL}/user/profile'
USER_URL_LOGIN_HISTORY = f'{BASE_URL}/user/profile/login_history'
USER_URL_CHANGE_LOGIN = f'{BASE_URL}/user/profile/change_login'
USER_URL_CHANGE_PASSWORD = f'{BASE_URL}/user/profile/change_password'

AUTH_URL_SIGN_UP = f'{AUTH_URL}/sign_up'
AUTH_URL_LOGIN = f'{AUTH_URL}/login'
AUTH_URL_LOGOUT = f'{AUTH_URL}/logout'
AUTH_URL_CHECK_ACCESS_TOKEN = f'{AUTH_URL}/check_access_token'
AUTH_URL_REFRESH = f'{AUTH_URL}/refresh'
