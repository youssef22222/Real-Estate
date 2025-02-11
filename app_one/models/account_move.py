from odoo import models,fields


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_do_something(self):
        #Write you logic here!
        print(self,"inside action_do_something method")