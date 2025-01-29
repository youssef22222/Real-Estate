from odoo import models,fields,api
from odoo.exceptions import ValidationError



class Property(models.Model):
    _name = 'property'
    name = fields.Char(required=True,default="New",size=20)
    description = fields.Text()
    postcode = fields.Char(required=True)
    date_availability = fields.Date()
    expected_price = fields.Float(required=True) #this required validation does not affect the Float fields
    selling_price = fields.Float(digits=(0,5))
    bedrooms = fields.Integer(required=True) #this required validation does not affect the Integer fields
    leaving_area = fields.Integer()
    facades = fields.Integer()
    garden = fields.Boolean(required=True)#this required validation does not affect the Boolean fields
    garage = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation=fields.Selection([
      #(name in database ,name that apear for the end user)
        ("north","North"),
        ("south","South"),
        ("east","East"),
        ("west","West")
    ],default="north")

    _sql_constraints = [
        ('unique_name', 'unique(name)','This name is Exist!'),
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_than_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError("Please add a valid number of bedrooms")
