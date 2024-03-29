from http import HTTPStatus

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from marshmallow import ValidationError

from api.v1.models.auth import login_in, login_out, sign_up_in
from services.auth.auth_service import (
    UserAlreadyExists,
    UserIncorrectLoginData,
    add_token_to_block_list,
    generate_token_pair,
    login_user,
    sign_up_user,
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign_up', methods=['POST'])
def sign_up():
    json_data = request.get_json()
    try:
        user = sign_up_in.load(json_data)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        sign_up_user(user)
        current_app.logger.info('User with email %s successfully signed in', user['login'])
    except UserAlreadyExists as err:
        current_app.logger.info('User with email %s denied to sign up: user already exists', user['login'])
        return jsonify(message=str(err)), HTTPStatus.CONFLICT

    return jsonify(msg='User created'), HTTPStatus.CREATED


@auth_bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    user_agent = request.headers.get('User-Agent', default='unknown device')
    try:
        user = login_in.load(json_data)
    except ValidationError as err:
        return jsonify(message=err.messages), HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        tokens = login_user(user['login'], user['password'], user_agent=user_agent)
        current_app.logger.info('User with email %s successfully logged in', user['login'])
    except UserIncorrectLoginData as err:
        current_app.logger.warning('User with email %s denied to login: incorrect login or password', user['login'])
        return jsonify(message=str(err)), HTTPStatus.UNAUTHORIZED

    return login_out.dump(tokens)


@auth_bp.route('/check_access_token', methods=['POST'])
@jwt_required()
def check_access_token():
    current_user = get_jwt().get('user_info')
    return jsonify(current_user), HTTPStatus.OK


@auth_bp.route('/logout', methods=['POST'])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    token_type = token['type']
    current_app.logger.info('Token_type: %s', token_type)
    add_token_to_block_list(token['jti'], token_type)

    return jsonify(msg=f'{token_type} token successfully revoked')


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    tokens = generate_token_pair(identity)

    return login_out.dump(tokens)
