from flask import Blueprint, request, jsonify
from pydantic import UUID4
from db.models import User
from api.v1.models.users import user

users = Blueprint("user", __name__)


@users.route('/profile/<user_id>', methods=['GET'])
def get_user_info(user_id: UUID4):
    user_db = User.query.filter_by(id=user_id).first()
    return jsonify(user.dump(user_db))



@users.route('/profile', methods=['PUT'])
def update_user_info():
    req = request.form.get("email")
    return jsonify(req)


@users.route('/profile/login_history/<user_id>', methods=['GET'])
def get_login_history(user_id):
    return f"User {user_id}"


@users.route('/profile/change_login/<user_id>>', methods=['PUT'])
def change_login(user_id):
    return f"User {user_id}"


@users.route('/profile/change_password/<user_id>>', methods=['PUT'])
def change_password(user_id):
    return f"User {user_id}"
