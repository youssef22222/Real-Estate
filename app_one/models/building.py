from odoo import models,fields


class Building(models.Model):
    _name = "building"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Building"

    name = fields.Char() # if there is no (name field or _rec_name field) the display name will be => (model name, id) => (building,1)
    #_rec_name = "code" # if you use this attribute the display name will be the code of building
    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()

    active = fields.Boolean(default=True)