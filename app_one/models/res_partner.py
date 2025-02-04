from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_id = fields.Many2one('property')
    price = fields.Float(related='property_id.selling_price')

    ##this is another way to make the related field
    # price = fields.Float(compute='_compute_price', store=True)
    #
    # @api.depends('property_id') # once you use store=True you should add this decorator
    # def _compute_price(self):
    #     for record in self:
    #         record.price = record.property_id.selling_price
