"""

Modified implementation of flask-expects-json under MIT license
https://pypi.org/project/flask-expects-json/

"""

from functools import wraps
from typing import Iterable

from flask import request, g, abort, current_app

from jsonschema import validate, ValidationError, FormatChecker


def expects_json(schema=None, ignore_for=None, check_formats=False):
    if schema is None:
        schema = dict()
    if ignore_for is not None:
        if isinstance(ignore_for, str):
            raise TypeError(
                'Methods should be wrapped in an iterable. i.e. ignore_for=["GET"]'
            )

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if ignore_for is not None and request.method in ignore_for:
                return f(*args, **kwargs)

            data = request.get_json(silent=True)

            if data is None:
                return abort(
                    400,
                    ValidationError(
                        "Please send valid JSON data with request."
                    ),
                )

            format_checker = None

            if check_formats:
                if isinstance(check_formats, Iterable):
                    format_checker = FormatChecker(check_formats)
                elif isinstance(check_formats, bool):
                    format_checker = FormatChecker()
                else:
                    return abort(400, "check_format must be bool or iterable")

            try:
                validate(data, schema, format_checker=format_checker)
            except ValidationError as e:
                return abort(400, e)

            g.data = data

            if hasattr(current_app, "ensure_sync"):
                return current_app.ensure_sync(f)(*args, **kwargs)
            else:
                return f(*args, **kwargs)

        return decorated_function

    return decorator
