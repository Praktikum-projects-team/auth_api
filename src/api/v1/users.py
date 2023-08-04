from http import HTTPStatus

from flask import Blueprint, jsonify, request, current_app, redirect
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from datetime import datetime

from api.v1.models.common import paginate_in
from api.v1.models.users import (
    change_login,
    change_password,
    login_history_paginated,
    user_change_data,
    user_schema,
    email_verify
)
from services.auth.auth_service import UserIncorrectPassword, change_user_pw
from services.user.user_service import (
    LoginAlreadyExists,
    user_change_login,
    user_get_data,
    user_login_history,
    user_update,
    verify_user_email,
    InvalidUser
)

users_bp = Blueprint("user", __name__)


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user_data = user_get_data(current_user)
    result = user_schema.dump(user_data)

    return jsonify(result), HTTPStatus.OK


@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_info():
    current_user = get_jwt_identity()
    user_new_data = request.get_json()
    try:
        body = user_change_data.load(user_new_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    user_update(current_user, body)
    current_app.logger.info('User with email %s updated', current_user)

    return {'message': 'User updated successfully'}, HTTPStatus.CREATED


@users_bp.route('/profile/login_history', methods=['GET'])
@jwt_required()
def get_login_history():
    current_user = get_jwt_identity()
    pagination = paginate_in.load(request.args)
    login_history_data = user_login_history(current_user, pagination.get('page'), pagination.get('page_size'))
    result = login_history_paginated.dump(login_history_data)
    return jsonify(result), HTTPStatus.OK


@users_bp.route('/profile/change_login', methods=['PUT'])
@jwt_required()
def change_user_login():
    current_user = get_jwt_identity()
    user_new_login = request.get_json()
    try:
        body = change_login.load(user_new_login)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    try:
        user_change_login(current_user, body)
        current_app.logger.info('User with email %s updated login successfully', current_user)
    except LoginAlreadyExists as err:
        current_app.logger.warning('User with email %s denied to change login: new login already exists', current_user)
        return jsonify(message=str(err)), HTTPStatus.CONFLICT

    return {'message': 'User login updated successfully'}, HTTPStatus.CREATED


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
        current_app.logger.info('User with email %s updated password successfully', current_user)
    except UserIncorrectPassword as err:
        current_app.logger.warning('User with email %s denied to change password: incorrect old password', current_user)
        return jsonify(message=str(err)), HTTPStatus.CONFLICT

    return {'message': 'User password updated successfully'}, HTTPStatus.CREATED


@users_bp.route('/email_verification', methods=['PUT'])
@jwt_required()
def verify_email():
    current_user = get_jwt_identity()
    user_verified_data = request.get_json()
    try:
        body = email_verify.load(user_verified_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    try:
        if datetime.utcnow() <= body['ttl']:
            verify_user_email(current_user, body)
        else:
            return {'message': 'Verification link has been expired'}, HTTPStatus.NOT_FOUND

        return redirect(body['redirect_link'])
    except InvalidUser as err:
        return err.messages, HTTPStatus.BAD_REQUEST
