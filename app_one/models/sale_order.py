from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    property_id = fields.Many2one('property')

    def action_confirm(self):
        result = super().action_confirm()
        print("inside action_confirm method") # write your logic here
        return result