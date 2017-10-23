from flask import jsonify


class ValidationError(ValueError):
    """Custom Exception"""
    pass

    # ======================================================
    # CUSTOM EXECPTIONS
    # ------------------------------------------------------


def forbidden(message):
    response = jsonify({'status': 403, 'error': 'forbidden',
                        'message': message})
    response.status_code = 403
    return response


def not_found(message):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': message})
    response.status_code = 404
    return response


def bad_request(message):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': message})
    response.status_code = 401
    return response


def Conflict(message):
    response = jsonify({'status': 409, 'error': 'conflict',
                        'message': message})
    response.status_code = 409
    return response

    # ======================================================
    # EOF
    # ------------------------------------------------------
