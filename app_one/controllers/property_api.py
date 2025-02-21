import json
import math
from urllib.parse import parse_qs
from odoo import http
from odoo.http import request
from .utility import valid_response, invalid_response


class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode("utf-8")
        vals = json.loads(args)

        if not vals.get("name"):
            return invalid_response("The name field is required.")

        try:
            result = request.env["property"].sudo().create(vals)

            if result:
                return valid_response("Property has been created successfully",{
                    "Property id": result.id,
                }, status=201)
        except Exception as error:
            return invalid_response(str(error))

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
                return invalid_response("The property with this id does not exist.")

            args = request.httprequest.data.decode("utf-8")
            vals = json.loads(args)
            property.sudo().write(vals)
            return valid_response("Property has been updated successfully",{})
        except Exception as error:
            return invalid_response(str(error))

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, property_id):
        try:
            property = request.env["property"].sudo().search([("id", "=", property_id)])
            if not property:
                return invalid_response("The property with this id does not exist.")

            return valid_response("Successfully retrieved property",{
                'id': property.id,
                'ref': property.ref,
                'name': property.name,
                'description': property.description,
                'postcode': property.postcode,
                'date_availability': property.date_availability,
                'bedrooms': property.bedrooms,
                'expected_price': property.expected_price,
            })
        except Exception as error:
            return invalid_response(str(error))

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property = request.env["property"].sudo().search([("id", "=", property_id)])
            if not property:
                return invalid_response("The property with this id does not exist.")
            property.sudo().unlink()
            return valid_response("Property has been deleted successfully",{})
        except Exception as error:
            return invalid_response(str(error))

    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def get_properties(self):
        try:
            properties = request.env["property"].sudo().search([])
            if not properties:
                return invalid_response("No properties found.")

            return valid_response("Successfully retrieved properties", [{
                'id': property.id,
                'ref': property.ref,
                'name': property.name,
                'description': property.description,
                'postcode': property.postcode,
                'date_availability': property.date_availability,
                'bedrooms': property.bedrooms,
                'expected_price': property.expected_price,
            } for property in properties])
        except Exception as error:
            return invalid_response(str(error))

    @http.route("/v1/properties/filter", methods=["GET"], type="http", auth="none", csrf=False)
    def get_properties_with_filter(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode("utf-8"))
            property_domain = [(key, "=", value[0]) for (key, value) in params.items()]

            properties = request.env["property"].sudo().search(property_domain)
            if not properties:
                return invalid_response("No properties found.")

            return valid_response("Successfully retrieved properties", [{
                'id': property.id,
                'ref': property.ref,
                'name': property.name,
                'description': property.description,
                'postcode': property.postcode,
                'date_availability': property.date_availability,
                'bedrooms': property.bedrooms,
                'state': property.state,
                'expected_price': property.expected_price,
            } for property in properties])
        except Exception as error:
            return invalid_response(str(error))

    @http.route("/v1/properties/filter/pagination", methods=["GET"], type="http", auth="none", csrf=False)
    def get_properties_with_filter_and_pagination(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode("utf-8"))
            property_domain = [(key, "=", value[0]) for (key, value) in params.items()
                if key in request.env["property"].fields_get()]

            page = offset = None
            limit = 5

            if params.get("page"):
                page = int(params["page"][0])
            if params.get("limit"):
                limit = int(params["limit"][0])

            if page:
                offset = (page - 1) * limit

            properties = request.env["property"].sudo().search(property_domain, offset=offset, limit=limit, order="id desc")
            property_count = request.env["property"].sudo().search_count(property_domain)

            if not properties:
                return invalid_response("No properties found.")

            return valid_response("Successfully retrieved properties", [{
                'id': property.id,
                'ref': property.ref,
                'name': property.name,
                'description': property.description,
                'postcode': property.postcode,
                'date_availability': property.date_availability,
                'bedrooms': property.bedrooms,
                'state': property.state,
                'expected_price': property.expected_price,
            } for property in properties], {
                "page no.": page if page else 1,
                "limit": limit,
                "no. of pages": math.ceil(property_count / limit) if limit else 1,
                "no. of records": property_count,
            })
        except Exception as error:
            return invalid_response(str(error))

    @http.route("/v1/property/sql", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        try:
            args = request.httprequest.data.decode("utf-8")
            vals = json.loads(args)

            if not vals.get("name"):
                return invalid_response("The name field is required.")

            cr = request.env.cr
            columns = ", ".join(vals.keys())
            values = ", ".join(['%s'] * len(vals))

            query = f"""
            INSERT INTO property ({columns}) VALUES ({values}) RETURNING id, {columns};
            """

            cr.execute(query, tuple(vals.values()))
            result = cr.fetchone()

            if result:
                return valid_response("Property has been created successfully",{
                    f"{key}" : result[idx] for idx, key in enumerate(["id"] + list(vals.keys()))
                }, status=201)
        except Exception as error:
            return invalid_response(str(error))


