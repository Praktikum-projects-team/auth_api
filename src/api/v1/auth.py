from http import HTTPStatus

from flask import jsonify
from flask import request
from flask import Blueprint


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from api.v1.models.auth import sign_up_in, login_in
from services.auth.auth_service import sign_up_user, login_user, UserAlreadyExists, NotExists

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

    access_token = create_access_token(identity=user.login)  # TODO improve tokens
    return jsonify(access_token=access_token)


@auth_bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, HTTPStatus.BAD_REQUEST
    try:
        user = login_in.load(json_data)
    except ValidationError as err:
        return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    try:
        tokens = login_user(user['login'], user['password'])
    except NotExists as err:
        return err, HTTPStatus.NOT_FOUND

    return tokens


# @app.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200

