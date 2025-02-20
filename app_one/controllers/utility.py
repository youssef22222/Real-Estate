from odoo.http import request


def valid_response(message, data, pagination=None, status=200):
    response_body = {
        "message": message,
        "data": data,
    }

    if pagination:
        response_body["meta_data"] = pagination

    return request.make_json_response(response_body, status=status)

def invalid_response(error, status=400):
    response_body = {
        "error": error,
    }

    return request.make_json_response(response_body, status=status)