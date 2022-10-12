from flask import jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException


def exception_handler(error):
    response = jsonify(detail=(error.message if hasattr(error, "message") else error.description))
    response.status_code = error.code if isinstance(error, HTTPException) else 500
    return response


class JSONExceptionHandler:

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.register(HTTPException)
        for code in default_exceptions.items():
            self.register(code)

    def register(self, exception_or_code, handler=None):
        self.app.add_error_handler(exception_or_code[0] if isinstance(exception_or_code, tuple) else exception_or_code,
                                   handler or exception_handler)
