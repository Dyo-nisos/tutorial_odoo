from odoo import models, fields


class Estate_Property_Tag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char(string='Etiqueta de propiedad',
                       required=True,
                       default="Nueva etiqueta..."
                       )
