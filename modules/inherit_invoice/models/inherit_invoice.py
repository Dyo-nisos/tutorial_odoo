from odoo import fields, models, api

class InheritedModel(models.Model):
    _inherit = "account.move"
    _description = "Inherited Model"
    
    quantity = fields.Integer(readonly=True)
    
    name = fields.Char(readonly=True)