import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID

from db.pg_db import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Role {self.name}(id: {self.id})>'


class User(db.Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    name = Column(String(100), nullable=True)
    is_superuser = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    roles = db.relationship(Role, secondary='user_roles')

    def __init__(self, login, password, name=None, is_superuser=False, email_verified=False, roles=None):
        self.login = login
        self.password = password
        self.name = name
        self.is_superuser = is_superuser
        self.email_verified = email_verified
        self.roles = roles or []

    def __repr__(self):
        return f'<User {self.login}>'


class LoginHistory(db.Model):
    __tablename__ = 'login_history'
    __table_args__ = (
        {
            'postgresql_partition_by': 'auth_datetime',
        }
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    user_agent = Column(String(250), nullable=False)
    auth_datetime = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, user_agent):
        self.user_id = user_id
        self.user_agent = user_agent

    def __repr__(self):
        return f'<LoginHistory {self.id} for user {self.user_id}>'


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), primary_key=True, nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey(Role.id, ondelete='CASCADE'), primary_key=True, nullable=False)
    given_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class OauthAccount(db.Model):
    __tablename__ = 'oauth_accounts'

    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), primary_key=True, nullable=False)
    oauth_user_login = Column(Text, nullable=False)
    provider = Column(String(100), primary_key=True, nullable=False)
