from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from api.v1.models.users import change_login, change_password, login_history, user_change_data, user_schema
from db.models import LoginHistory, User
from db.pg_db import db
from db.queries import user
from services.auth.auth_service import UserIncorrectPassword, change_user_pw

users_bp = Blueprint("user", __name__)


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user = User.query.filter_by(login=current_user).first()
    result = user_schema.dump(user)
    return jsonify(result), HTTPStatus.OK


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
    user.name = body['name']
    db.session.commit()
    return {"message": "User updated successfully"}, HTTPStatus.CREATED


@users_bp.route('/profile/login_history', methods=['GET'])
@jwt_required()
def get_login_history():
    current_user = get_jwt_identity()
    user_id = User.query.filter_by(login=current_user).first().id
    user_login_history = LoginHistory.query.filter_by(user_id=user_id).all()
    result = login_history.dump(user_login_history)
    return jsonify(result), HTTPStatus.OK


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
    try:
        change_user_pw(current_user, body['old_password'], body['new_password'])
    except UserIncorrectPassword as err:
        return jsonify(message=str(err)), HTTPStatus.CONFLICT
    return {"message": "User password updated successfully"}, HTTPStatus.CREATED
