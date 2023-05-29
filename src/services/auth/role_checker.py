import functools
from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

from constants import RoleName
from db.queries.user import get_user_by_login


def role_required(role):
    def role_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_login = get_jwt_identity()
            user = get_user_by_login(user_login)
            role_names = [r.name for r in user.roles]
            if role not in role_names:
                return jsonify(message=f'user must have role {role}'), HTTPStatus.FORBIDDEN
            result = func(*args, **kwargs)
            return result
        return wrapper
    return role_decorator


admin_required = role_required('admin')
