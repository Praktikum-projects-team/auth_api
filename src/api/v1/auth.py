from flask import jsonify
from flask import request
from flask import Blueprint


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

#
# @auth_bp.route('/login', methods=['POST'])
# def login():
#     username = request.json.get("username", None)
#     password = request.json.get("password", None)
#
#
#     access_token = create_access_token(identity=username)
#     return jsonify(access_token=access_token)
#
#
# @app.route("/protected", methods=["GET"])
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
#
#
# @app.route('/api/hello-world')
# def hello_world():
#     from db.models import User
#     user = User.query.filter_by(login='admin').first()
#     return str(user.id)
