from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare


class Estate_Property_Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True,
        ondelete='cascade'
    )
    
#     Related fields
# A special case of computed fields are related (proxy) fields, which provide the value of a sub-field on the current record. They are defined by setting the related parameter and like regular computed fields they can be stored:

# nickname = fields.Char(related='user_id.partner_id.name', store=True)
# The value of a related field is given by following a sequence of relational fields and reading a field on the reached model. The complete sequence of fields to traverse is specified by the related attribute.

# Some field attributes are automatically copied from the source field if they are not redefined: string, help, required (only if all fields in the sequence are required), groups, digits, size, translate, sanitize, selection, comodel_name, domain, context. All semantic-free attributes are copied from the source field.

# By default, related fields are:

# not stored

# not copied

# readonly

# computed in superuser mode

# Add the attribute store=True to make it stored, just like computed fields. Related fields are automatically recomputed when their dependencies are modified.

    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property type',
        related='property_id.property_type_id',
        store=True
    )

    name = fields.Char(string='Oferta de propiedad',
                       required=True,
                       default="Nueva oferta...",
                       copy=False
                       )

    price = fields.Float(string='Precio',
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
        '''Se crea una variable existing_accepted, con self.env accedemos al modelo especificado
        buscamos registros desde la base de datos y encontramos mientras la foranea de la tabla estate_property_offer
        sea igual a los ids de '''
        existing_accepted = self.search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
            ('id', '!=', self.id)
        ])
        
        if existing_accepted:
            raise UserError(
                "Ya se aceptó otra oferta para esta propiedad. "
                "Solo puede haber una oferta aceptada por propiedad."
            )
        for record in self:
            if float_compare(record.price, record.property_id.expected_price * 0.9,5) == -1:
            # if float_compare(5.8,5.9,1) == -1:
                raise UserError('''Hola si El precio debe ser de por lo
menos mayor al el 90% del precio esperado
debe ser de miniamo: ''' + str(record.property_id.expected_price * 0.9))
            record.status = 'accepted'
            self.property_id.selling_price = record.price
            self.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offerAccepted'
    
    @api.depends("property_id.selling_price")
    def refuse_property(self):
        for record in self:
            record.status = 'refused'
    
    @api.model
    # # self es el modelo, no un recordset
    def create(self,vals):
    #     print(type(self.price))
    #     print(vals['price'])
    #     print("\n")
    #     print(self.env['estate.property'].browse(vals['property_id']).expected_price)
        property_objeto = self.env['estate.property'].browse(vals['property_id'])
        property_objeto.state='offerReceived'
    #     # if float_compare(property_objeto.expected_price * 0.9, 6) == -1:
    #     if float_compare(property_objeto.expected_price * 0.9, vals['price'], 1) == 1:
    #         raise UserError("El precio de oferta debe ser al menos del 90% del precio esperado\n"
    #                         "minimo: " + str(property_objeto.expected_price * 0.9))
        return super(Estate_Property_Offer, self).create(vals)
    
    #OJO: Una oferta aceptada no puede ser editada
    
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if float_compare(record.property_id.expected_price * 0.9, record.price, 1) == 1:
                raise UserError("El precio de oferta debe ser al menos del 90% del precio esperado\n"
                                "minimo: " + str(record.property_id.expected_price * 0.9))

    def ver_relaciones(self):
        for record in self:
            print("ID de la propiedad:", record.property_id.id)
            print("Tipo de propiedad:", record.property_type_id.name)
            print("ID del partner:", record.partner_id.id)
            print("Nombre del partner:", record.partner_id.name)
            print("Precio esperado de la propiedad:", record.property_id.expected_price)
            print("Precio de venta de la propiedad:", record.property_id.selling_price)