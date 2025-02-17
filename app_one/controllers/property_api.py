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

    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def put_property(self, property_id):
        try:
            property = request.env["property"].sudo().search([("id", "=", property_id)])
            if not property:
                return request.make_json_response({
                    "error": "The property with this id does not exist.",
                }, status=400)

            args = request.httprequest.data.decode("utf-8")
            vals = json.loads(args)
            property.sudo().write(vals)
            return request.make_json_response({
                "message": "Property has been updated successfully",
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": str(error),
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        try:
            property = request.env["property"].sudo().search([("id", "=", property_id)])
            if not property:
                return request.make_json_response({
                    "error": "The property with this id does not exist.",
                }, status=400)

            return request.make_json_response({
                'id': property.id,
                'ref': property.ref,
                'name': property.name,
                'description': property.description,
                'postcode': property.postcode,
                'date_availability': property.date_availability,
                'bedrooms': property.bedrooms,
                'expected_price': property.expected_price,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": str(error),
            },status=400)

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property = request.env["property"].sudo().search([("id", "=", property_id)])
            if not property:
                return request.make_json_response({
                    "error": "The property with this id does not exist.",
                }, status=400)

            property.sudo().unlink()
            return request.make_json_response({
                'message': 'Property has been deleted successfully',
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": str(error),
            }, status=400)