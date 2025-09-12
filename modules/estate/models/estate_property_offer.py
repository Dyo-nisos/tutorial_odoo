from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class Estate_Property_Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True,
        ondelete='cascade'
        )

    name = fields.Char(string='Oferta de propiedad',
                       required=True,
                       default="Nueva oferta...",
                       copy=False
                       )

    price = fields.Integer(string='Precio',
                           required=True,
                           default=0,
                           copy=False,
                           )

    partner_id = fields.Many2one('res.partner',
                                 required=True,
                                 string="Partner",
                                 copy=False,
                                 )

    create_date = fields.Date(string='Date found',
                              default=fields.Datetime.now()
                              )

    status = fields.Selection(
        selection=[
            ('accepted', 'Aceptado'),
            ('refused', 'Rechazado'),
        ],
        string='Status', copy=False
    )

    validity = fields.Integer(string='Valido',
                              required=False,
                              default=7
                              )

    date_deadline = fields.Date(string='Fecha de vencimiento',
                                compute="_sum_create_date_validity"
                                )

    def _sum_create_date_validity(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                    )

    def accept_property(self):
        for record in self:
            if float_compare(record.price, record.property_id.expected_price * 0.9,5) == -1:
                raise ValidationError('''El precio debe ser de por lo
menos mayor al el 90% del precio esperado
debe ser de miniamo: ''' + str(record.property_id.expected_price * 0.9))
            record.status = 'accepted'
            self.property_id.selling_price = record.price
            self.property_id.buyer_id = record.partner_id

    @api.depends("property_id.selling_price")
    def refuse_property(self):
        for record in self:
            record.status = 'refused'
