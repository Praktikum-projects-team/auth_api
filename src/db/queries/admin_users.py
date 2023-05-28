from http import HTTPStatus
from uuid import UUID

from sqlalchemy.exc import DataError

from db.models import Role, UserRole


def get_user_roles_by_user_id(user_id: UUID):
    try:
        user_roles = UserRole.query.filter_by(user_id=user_id).all()
    except (ValueError, DataError) as err:
        return {"message": str(err)}, HTTPStatus.BAD_REQUEST

    result_user_roles = list()
    for role in user_roles:
        role_data = Role.query.filter_by(id=role.role_id).first()
        result_user_roles.append(role_data.name)

    return result_user_roles
