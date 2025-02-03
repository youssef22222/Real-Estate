from odoo import models,fields


class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required=True)
    phone = fields.Char()
    address = fields.Char()

    property_ids = fields.One2many('property', 'owner_id')

    _sql_constraints = [
        # this constraint will not be applied if there is duplicate in the name column in the database
        ('unique_name', 'unique(name)', 'This name is Exist!')
    ]