import pytest

# Регистрация чекеров в pytest
pytest.register_assert_rewrite('tests.functional.utils.checkers')

# Регистрация фикстур в pytest
pytest_plugins = ('tests.functional.fixtures.pg', 'tests.functional.fixtures.admin')
