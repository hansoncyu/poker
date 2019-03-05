from functools import wraps

from cerberus import Validator
from flask import request
from werkzeug.exceptions import BadRequest


def validate_body(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            validator = Validator(schema)
            if not validator.validate(request.form.to_dict()):
                raise BadRequest(validator.errors)

            return func(validator.document, *args, **kwargs)

        return wrapper

    return decorator
