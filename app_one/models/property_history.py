from odoo import models,fields


class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'Property History'

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')

    old_state = fields.Char()
    new_state = fields.Char()

    datetime = fields.Datetime()

    reason = fields.Char()

    line_ids = fields.One2many('property.history.line', 'history_id')


class PropertyHistoryLine(models.Model):
    _name = 'property.history.line'

    history_id = fields.Many2one('property.history')
    description = fields.Char()
    area = fields.Char()
