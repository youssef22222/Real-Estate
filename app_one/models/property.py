from odoo import models,fields

class Property(models.Model):
    _name = 'property'
    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    leaving_area = fields.Integer()
    facades = fields.Integer()
    garden = fields.Boolean()
    garage = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation=fields.Selection([
      #(name in database ,name that apear for the end user)
        ("north","North"),
        ("south","South"),
        ("east","East"),
        ("west","West")
    ])
