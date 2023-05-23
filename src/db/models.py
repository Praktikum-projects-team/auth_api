import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from db.pg_db import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Role {self.name}(id: {self.id})>'


class User(db.Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    name = Column(String, nullable=True)
    is_superuser = Column(Boolean, default=False)
    roles = db.relationship(Role, secondary='user_roles')

    def __init__(self, login, password, name=None, is_superuser=False):
        self.login = login
        self.password = password
        self.name = name
        self.is_superuser = is_superuser

    def __repr__(self):
        return f'<User {self.login}>'


class LoginHistory(db.Model):
    __tablename__ = 'login_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    user_agent = Column(String, nullable=False)
    auth_datetime = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, user_agent):
        self.user_id = user_id
        self.user_agent = user_agent

    def __repr__(self):
        return f'<LoginHistory {self.id} for user {self.user_id}>'


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), primary_key=True, nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey(Role.id), primary_key=True, nullable=False)
    given_at = Column(DateTime, nullable=False, default=datetime.utcnow)
