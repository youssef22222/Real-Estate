from odoo import models,fields,api
from odoo.exceptions import ValidationError



class Property(models.Model):
    _name = 'property'
    _inherit = ['mail.thread', 'mail.activity.mixin'] #odoo support multi inheritance
    _description = 'Property' # this name will appear in the chatter when create new property

    name = fields.Char(required=True,default="New",size=20)
    description = fields.Text(tracking=True)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=True)
    expected_selling_date = fields.Date()
    is_late = fields.Boolean()
    expected_price = fields.Float(required=True) #this required validation does not affect the Float fields
    selling_price = fields.Float(tracking=True)
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
        ("closed","Closed"),
    ],default="draft")

    active = fields.Boolean(default=True)

    owner_id =fields.Many2one('owner')
    owner_address = fields.Char(related="owner_id.address", store=True) #store=True will store the field in the property table
    owner_phone = fields.Char(related="owner_id.phone", readonly=False) #readonly=False enable you to update this field form the property model

    tag_ids = fields.Many2many('tag')

    line_ids = fields.One2many('property.line', 'property_id')

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

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

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

    def check_expected_selling_date(self):
        properties = self.search([])
        for property in properties:
            if property.expected_selling_date and property.expected_selling_date < fields.date.today():
                property.is_late = True

    def discover_env_object(self):
        print(self.env) #<odoo.api.Environment object at 0x743238187340>
        print(self.env.user) #res.users(2,)
        print(self.env.user.id) #2
        print(self.env.user.login) # print user email => admin
        print(self.env.uid) # print user id directly without user object => 2
        print(self.env.company) #res.company(1,)
        print(self.env.company.name) #YourCompany (name)
        print(self.env.company.id) #1
        print(self.env.company.street) #250 Executive Park Blvd, Suite 3400
        print(self.env.context) #{'params': {'id': 1, 'cids': 1, 'menu_id': 538, 'action': 681, 'model': 'property', 'view_type': 'form'}, 'lang': 'en_US', 'tz': 'Europe/Brussels', 'uid': 2, 'allowed_company_ids': [1]}
        print(self.env.cr) #<odoo.sql_db.Cursor object at 0x7953515d1a50>
        print(self.env['owner']) #owner()
        print(self.env['owner'].create({
            "name":"Owner one",
            "phone":"012345489",
            "address":"Cairo",
        })) #owner(9,)
        print(self.env['owner'].search([])) #owner(1, 2, 3, 8, 9)


    class PropertyLine(models.Model):
        _name = 'property.line'

        area = fields.Float()
        description = fields.Char()

        property_id = fields.Many2one('property')