import json
from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode("utf-8")
        vals = json.loads(args)

        if not vals.get("name"):
            return request.make_json_response({
                "error": "The name field is required.",
            }, status=400)

        try:
            result = request.env["property"].sudo().create(vals)

            if result:
                return request.make_json_response({
                    "message": "Property has been created successfully",
                    "Property id": result.id,
                }, status=201)
        except Exception as error:
            return request.make_json_response({
                "error": str(error),
            }, status=400)

    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode("utf-8")
        vals = json.loads(args)

        if not vals.get("name"):
            return {
                "error": "The name field is required.",
            }

        try:
            result = request.env["property"].sudo().create(vals)

            if result:
                # With type="json" you can return dictionary or list of dictionaries
                return {
                    "message": "Property has been created successfully",
                    "Property id": result.id,
                }
        except Exception as error:
            return {
                "error": str(error),
            }