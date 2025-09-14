from odoo import models, fields


class Estate_Property_Type(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(string='Tipo de propiedad',
                       required=True,
                       default="Nuevo tipo..."
                       )

    sequence = fields.Integer(string='Sequence', default=1)

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string='Propiedades',
        required=True
    )

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string='Ofertas',
        required=True
    )

    offer_count = fields.Integer(
        string="Cantidad de ofertas",
        compute="_count_offers"
    )
    _sql_constraints = [(
            'checkear_unique_name',
            'unique(name)',
            'Se espera que el nombre sea unico, pruebe con otro'
            )]
    
    def _count_offers(self):
        for r in self:
            r.mapped('offer_ids')