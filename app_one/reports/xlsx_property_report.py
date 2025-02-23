from ast import literal_eval
from odoo import http
from odoo.http import request
import xlsxwriter
import io


class XlsxPropertyReport(http.Controller):

    @http.route("/v1/property/excel/report/<string:property_ids>", type="http", auth="user")
    def download_property_excel_report(self, property_ids):
        property_ids = literal_eval(property_ids)
        properties = request.env["property"].browse(property_ids)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Properties")

        header_format = workbook.add_format({"bold": True, "bg_color": "#D3D3D3", "border": 1, "align": "center"})
        string_format = workbook.add_format({"border": 1, "align": "center"})
        price_format = workbook.add_format({"num_format": "$##,##00.00","border": 1, "align": "center"})

        worksheet.set_column("A:Z", 20) # set the width of all columns to 20 characters

        fields = {
            "Name":"name",
            "Postcode":"postcode",
            "Selling Price":"selling_price",
            "Garden":"garden",
        }

        for col_num, header in enumerate(fields.keys()):
            worksheet.write(0, col_num, header, header_format)

        for row_num, property in enumerate(properties):
            for col_num, field in enumerate(fields.values()):
                if field == "selling_price":
                    worksheet.write(row_num + 1, col_num, getattr(property, field), price_format)
                elif field == "garden":
                    worksheet.write(row_num + 1, col_num, "Yes" if getattr(property, field) else "No", string_format)
                else:
                    worksheet.write(row_num + 1, col_num, getattr(property, field), string_format)

        workbook.close()
        output.seek(0)

        file_name = "property Report.xlsx"

        return request.make_response(
            output.getvalue(),
            headers = [
                ("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                ("Content-Disposition", f"attachment; filename={file_name}")
            ]
        )


