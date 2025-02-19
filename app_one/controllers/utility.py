from odoo.http import request


def valid_response(message, data, status=200):
    response_body = {
        "message": message,
        "data": data,
    }

    return request.make_json_response(response_body, status=status)

def invalid_response(error, status=400):
    response_body = {
        "error": error,
    }

    return request.make_json_response(response_body, status=status)