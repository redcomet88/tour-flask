from flask import jsonify

def make_response(data=None, code=0, message='Success'):
    response = {
        'code': code,
        'message': message,
        'data': data if data is not None else []
    }
    return jsonify(response)
