from odoo import models, fields


class Estate_Property_Tag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name desc'

    name = fields.Char(string='Etiqueta de propiedad',
                       required=True,
                       default="Nueva etiqueta..."
                       )
    
    color = fields.Integer(string='Color')
