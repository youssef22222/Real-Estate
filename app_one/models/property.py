from odoo import models,fields,api
from odoo.exceptions import ValidationError



class Property(models.Model):
    _name = 'property'
    name = fields.Char(required=True,default="New",size=20)
    description = fields.Text()
    postcode = fields.Char(required=True)
    date_availability = fields.Date()
    expected_price = fields.Float(required=True) #this required validation does not affect the Float fields
    selling_price = fields.Float()
    diff = fields.Float(compute="_compute_diff", store=True, readonly=False)
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

    state = fields.Selection([
        ("draft","Draft"),
        ("pending","Pending"),
        ("sold","Sold"),
    ],default="draft")

    owner_id =fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')

    _sql_constraints = [
        ('unique_name', 'unique(name)','This name is Exist!'),
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_than_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError("Please add a valid number of bedrooms")

    @api.model_create_multi
    def create(self, vals):
        result = super().create(vals)
        #result = super(Property,self).create(vals) #also you can use this way for old versions of python
        print("inside create method") #write your logic here, you can change in the result Ex. result.name = "property 100"
        return result

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        result = super()._search(domain, offset, limit, order, access_rights_uid)
        print("inside _search method") #write your logic here
        return result

    def write(self, vals):
        result = super().write(vals)
        print("inside write method") #write you logic here
        return result

    def unlink(self):
        result = super().unlink()
        print("inside unlink method") #write your logic here
        return result

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.write({
                'state': 'pending',
            })

    def action_sold(self):
        for rec in self:
            rec.state = 'sold'

    #Here you can depend on any field in the model or depend on the related filed like owner_id.phone
    @api.depends('selling_price','expected_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    #Any change happen in the expected_price field in the UI this method will be called
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            if rec.expected_price < 0 :
                return {
                    "warning":{
                        "title":"warning",
                        "message":"Negative value not allowed for expected price",
                        "type": "notification"},
                }
                #Note this warning will appear if the user enter negative value to expected_price field
                #Even if the user enter negative value to expected_price field it will be saved in database
