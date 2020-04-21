from flask import jsonify

class InvalidData(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def make_error(status_code: int, message: str):
    response = jsonify({
        'status_code': status_code,
        'message': message
    })
    response.status_code = status_code
    return response

