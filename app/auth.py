from datetime import datetime, timedelta
from jose import jwt
from flask import current_app


def encode_token(customer_id):
    payload = {
        "sub": customer_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return token
