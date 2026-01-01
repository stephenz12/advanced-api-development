from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "user_id" not in data:
        return jsonify({"error": "user_id required"}), 400

    token = create_access_token(identity=data["user_id"])
    return jsonify({"access_token": token}), 200
