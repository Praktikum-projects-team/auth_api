from constants import RoleName
from core.config import AppConfig
from db.models import Role, User, UserRole
from db.pg_db import db

app_conf = AppConfig()


def createsuperuser():
    user_exist = db.session.query(User).filter(User.login == app_conf.superuser_login).first()
    if user_exist:
        return "Superuser already exist"

    superuser = User(login=app_conf.superuser_login, password=app_conf.superuser_password, is_superuser=True)
    db.session.add(superuser)
    db.session.commit()

    role_exist = db.session.query(Role).filter(Role.name == RoleName.ADMIN).first()
    if not role_exist:
        role = Role(name=RoleName.ADMIN)
        db.session.add(role)
        db.session.commit()

    role_id = db.session.query(Role.id).filter_by(name=RoleName.ADMIN).scalar()

    user_role = UserRole(user_id=superuser.id, role_id=role_id)
    db.session.add(user_role)
    db.session.commit()
    return "Superuser successfully created"
