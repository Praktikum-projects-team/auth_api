import functools
import json
from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def role_required(required_role):
    def role_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user = json.loads(claims.get('user_info'))

            if not user['is_superuser'] and required_role not in user['roles']:
                return jsonify(message=f'user must have role {required_role}'), HTTPStatus.FORBIDDEN
            result = func(*args, **kwargs)

            return result
        return wrapper
    return role_decorator


admin_required = role_required('admin')
