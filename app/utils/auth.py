from jose import jwt, JWTError
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from app.models import Customer
from app.extensions import db

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"


# =========================
# CREATE TOKEN
# =========================
def encode_token(customer_id):
    payload = {
        "sub": str(customer_id),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# =========================
# TOKEN REQUIRED DECORATOR
# =========================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Missing Authorization Header"}), 401

        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            customer_id = int(decoded["sub"])
        except (JWTError, IndexError):
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(customer_id, *args, **kwargs)

    return decorated
