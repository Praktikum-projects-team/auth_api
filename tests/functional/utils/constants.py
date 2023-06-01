class RoleName:
    ADMIN = "admin"
    USER = "user"


class AdminData:
    LOGIN = "admin@test.ru"
    PASSWORD = "123qwe"


class UserData:
    LOGIN = "user@test.ru"
    PASSWORD = "123qwe"
    NAME = "test_user"


USER_DATA_DEFAULT = {'login': UserData.LOGIN, 'password': UserData.PASSWORD}
