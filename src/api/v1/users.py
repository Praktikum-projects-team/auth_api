from flask import Blueprint, request, jsonify
from pydantic import UUID4
from db.models import User, LoginHistory
from db.pg_db import db
from db.queries import user
from api.v1.models.users import user_schema, user_change_data, change_login, change_password, login_history
import logging
from sqlalchemy.exc import DataError
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from services.auth.auth_service import change_user_pw, UserIncorrectPassword

users_bp = Blueprint("user", __name__)


@users_bp.route('/profile/<user_id>', methods=['GET'])
@jwt_required()
def get_user_info(user_id: UUID4):
    try:
        user = User.query.filter_by(id=user_id).first()
    except (ValueError, DataError) as err:
        return {"message": str(err)}, HTTPStatus.BAD_REQUEST
    if not user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND
    result = user_schema.dump(user)
    return jsonify(result)


@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_info():
    current_user = get_jwt_identity()
    user = User.query.filter_by(login=current_user).first()
    user_new_data = request.get_json()
    try:
        body = user_change_data.load(user_new_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST
    if body['name']:
        user.name = body['name']
    db.session.commit()
    return {"message": "User updated successfully"}, HTTPStatus.CREATED


@users_bp.route('/profile/login_history/<user_id>', methods=['GET'])
@jwt_required()
def get_login_history(user_id: UUID4):
    try:
        user_login_history = LoginHistory.query.filter_by(user_id=user_id).all()
    except (ValueError, DataError) as err:
        return {"message": str(err)}, HTTPStatus.BAD_REQUEST
    if not user_login_history:
        return {"message": "Login history not found"}, HTTPStatus.NOT_FOUND
    result = login_history.dump(user_login_history)
    return jsonify(result)


@users_bp.route('/profile/change_login', methods=['PUT'])
@jwt_required()
def change_user_login():
    current_user = get_jwt_identity()
    user_data = User.query.filter_by(login=current_user).first()
    user_new_login = request.get_json()
    try:
        body = change_login.load(user_new_login)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST
    login_exist = user.does_user_exist(body['new_login'])
    if login_exist:
        return {"message": "Login already exist"}, HTTPStatus.CONFLICT
    elif body['new_login']:
        user_data.login = body['new_login']
    db.session.commit()
    return {"message": "User login updated successfully"}, HTTPStatus.CREATED


@users_bp.route('/profile/change_password', methods=['PUT'])
@jwt_required()
def change_user_password():
    current_user = get_jwt_identity()
    user_password_data = request.get_json()
    try:
        body = change_password.load(user_password_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST
    if body['new_password']:
        try:
            user_data = change_user_pw(current_user, body['old_password'], body['new_password'])
        except UserIncorrectPassword as err:
            return jsonify(message=str(err)), HTTPStatus.CONFLICT
        db.session.commit()
        return {"message": "User password updated successfully"}, HTTPStatus.CREATED
    else:
        return {"message": "User password must not be empty"}, HTTPStatus.CONFLICT
