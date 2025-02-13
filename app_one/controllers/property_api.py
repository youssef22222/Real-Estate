import json
from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode("utf-8")
        vals = json.loads(args)

        result = request.env["property"].sudo().create(vals)

        if result:
            return request.make_json_response({
                "message": "Property has been created successfully",
                "Property id": result.id,
            }, status=201)