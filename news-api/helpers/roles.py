from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_roles = claims.get('role', [])
            if not any(role in user_roles for role in roles):
                return jsonify(msg="Access forbidden: insufficient privileges"), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator