from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

def token_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        customer_id = int(get_jwt_identity())  # convert back to int
        return fn(customer_id, *args, **kwargs)
    return wrapper
