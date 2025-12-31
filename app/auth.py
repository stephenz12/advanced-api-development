from flask_jwt_extended import jwt_required, create_access_token
from functools import wraps


def encode_token(customer_id):
    return create_access_token(identity=customer_id)


def token_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper
