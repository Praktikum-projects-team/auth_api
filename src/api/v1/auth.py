from http import HTTPStatus

from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from marshmallow import ValidationError

from api.v1.models.auth import sign_up_in, login_in, login_out
from services.auth.auth_service import (
    sign_up_user,
    login_user,
    UserAlreadyExists,
    UserIncorrectLoginData,
    add_token_to_block_list
)


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign_up', methods=['POST'])
def sign_up():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, HTTPStatus.BAD_REQUEST
    try:
        user = sign_up_in.load(json_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        sign_up_user(user)
    except UserAlreadyExists as err:
        return str(err), HTTPStatus.CONFLICT

    return 'user created', HTTPStatus.OK


@auth_bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    user_agent = request.headers.get('User-Agent', default='unknown device')
    if not json_data:
        return {"message": "No input data provided"}, HTTPStatus.BAD_REQUEST
    try:
        user = login_in.load(json_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        tokens = login_user(user['login'], user['password'], user_agent=user_agent)
    except UserIncorrectLoginData as err:
        return err, HTTPStatus.UNAUTHORIZED

    return login_out.dump(tokens)


# @auth_bp.route('/check_token', methods=['POST'])
# @jwt_required()
# def check_token():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    add_token_to_block_list(token['jti'])
    return jsonify(msg=f'{token["type"].capitalize()} token successfully revoked')


# @auth_bp.route('/refresh', methods=['POST'])
# @
# def refresh():
#     user_agent = request.headers.get('User-Agent', default='unknown device')
#     try:
#         tokens = refresh_token()
#     except UserIncorrectLoginData as err:
#         return err, HTTPStatus.UNAUTHORIZED
#
#     return login_out.dump(tokens)

