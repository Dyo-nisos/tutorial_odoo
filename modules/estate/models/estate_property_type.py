from odoo import models, fields


class Estate_Property_Type(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(string='Tipo de propiedad',
                       required=True,
                       default="Nuevo tipo..."
                       )

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string='Propiedades',
        ondelete='cascade'
    )

    _sql_constraints = [(
            'checkear_unique_name',
            'unique(name)',
            'Se espera que el nombre sea unico, pruebe con otro'
            )]