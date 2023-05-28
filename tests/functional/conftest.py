import pytest

# Регистрация чекеров в pytest
pytest.register_assert_rewrite('tests.functional.utils.checkers')

pytest_plugins = ('tests.functional.fixtures.pg',)
