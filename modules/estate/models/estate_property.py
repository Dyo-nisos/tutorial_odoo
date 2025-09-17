from odoo import models, fields, api
from odoo.exceptions import ValidationError

''' 
Tabla Propiedad inmobiliaria

Esto se representa de la siguiente forma:
 id                 | integer                     |           | not null | nextval('estate_property_id_seq'::regclass)
 bedrooms           | integer                     |           |          | 
 living_area        | integer                     |           |          | 
 facades            | integer                     |           |          | 
 garden_area        | integer                     |           |          | 
 create_uid         | integer                     |           |          | 
 write_uid          | integer                     |           |          | 
 name               | character varying           |           | not null | 
 postcode           | character varying           |           |          | 
 garden_orientation | character varying           |           |          | 
 date_availability  | date                        |           |          | 
 description        | text                        |           |          | 
 garage             | boolean                     |           |          | 
 garden             | boolean                     |           |          | 
 create_date        | timestamp without time zone |           |          | 
 write_date         | timestamp without time zone |           |          | 
 expected_price     | double precision            |           | not null | 
 selling_price      | double precision            |           |          | 
 active             | boolean                     |           |          | 
 state              | character varying           |           |          | 
 property_type_ids  | integer                     |           |          | 
 buyer_id           | integer                     |           |          | 
 salesperson_id     | integer                     |           |          | 
'''
class Estate_Property(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    name = fields.Char(string='Propiedad',
        required=True,
        default="Nueva propiedad..."
    )

    description = fields.Text(string='Descripcion')
    property_type_id = fields.Many2one('estate.property.type',
        string="Tipo",
        required=True
    )

    buyer_id = fields.Many2one('res.partner',
        string="Comprador",
        copy=False,
        readonly=True
    )

    tag_ids = fields.Many2many('estate.property.tag',
                               string="Etiqueta",
                               copy=False
                               )
    
    is_sold_canceled = fields.Boolean(string='sold_canceled', default=False)
    

    offer_ids = fields.One2many('estate.property.offer',
        inverse_name='property_id',
        string="Oferta",
        copy=False,
    )

    salesperson_id = fields.Many2one('res.users',
        string="Vendedor",
        default=lambda self: self.env.user
    )

    postcode = fields.Char(string='Codigo postal')
    date_availability = fields.Date(string='Disponible desde',
        copy=False,
        default=fields.Datetime.now
    )

    expected_price = fields.Float(string='Precio esperado', required=True)
    selling_price = fields.Float(string='Precio de venta',
                                 readonly=True,
                                 copy=False)

    bedrooms = fields.Integer(string='Dormitorios', default=2)
    living_area = fields.Integer(string='Area habitable (m)')
    facades = fields.Integer(string='Fachada')
    garage = fields.Boolean(string='Garaje', default=False, copy=False)
    garden = fields.Boolean(string='Jardin', default=False, copy=False)
    garden_area = fields.Integer(string='Area del jardin (m)')

    garden_orientation = fields.Selection(
        selection=[
            ('north', 'Norte'),
            ('south', 'Sur'),
            ('east', 'Este'),
            ('west', 'Oeste')
        ],
        string='Orientacion de Jardin'
    )

    active = fields.Boolean(string="Activo", default=True)
    state = fields.Selection(
        selection=[
            ('New', 'Nuevo'),
            ('offerReceived', 'Oferta recibida'),
            ('offerAccepted', 'Oferta aceptada'),
            ('sold', 'Vendida'),
            ('canceled', 'Cancelada')
        ], string='Estado', default="New", copy=False
    )

    total_area = fields.Integer(compute="_sum_living_garden", string='Area total')
    best_offer = fields.Integer(compute="_best_offer", string= 'Mejor oferta')

    """
    Metodos relacionados con un campo
    """

    @api.depends('living_area', 'garden_area')
    def _sum_living_garden(self):
        self.total_area = self.living_area + self.garden_area


    @api.onchange("garden")
    def _auto_fill(self):
        for record in self:
            if record.garden is True:
                record.garden_orientation = 'north'
                record.garden_area = 10
            else:
                record.garden_orientation = ''
                record.garden_area = 0
                record.garden_orientation 

    def sold_property(self):
        for record in self:
            if record.state == 'canceled':
                raise ValidationError('Una propiedad que ha sido cancelada no puede ser vendida')
            else:
                if record.state == 'offerAccepted':
                    record.state = 'sold' 
                    record.is_sold_canceled = True
                else:
                    raise ValidationError('Solo se pueden vender propiedades con oferta aceptada')

    def canceled_property(self):
        for record in self:
            record.state = 'canceled'
            record.is_sold_canceled = True

    @api.depends('offer_ids.price')
    def _best_offer(self):
        for record in self:
            arr_price = record.mapped('offer_ids.price')
            if arr_price is None or len(arr_price) == 0:
                record.best_offer = 0
            else:
                record.best_offer = max(arr_price)

    """
    Constraints del modelo
    """

    _sql_constraints = [(
        'checkear_expected_price',
        'check(expected_price > 0)',
        'Hola, el precio no puede ser negativo o cero'
        )]
    

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_property_is_not_new_canceled(self):
        for r in self:
            if not (r.state == 'New' or r.state == 'canceled'):
                raise ValidationError("Solo se pueden eliminar propiedades con estado Nuevo o Cancelado")

    def ver_relaciones(self):
        for record in self:
            print("ID del vendedor:", record.salesperson_id.id)
            print("Nombre del vendedor:", record.salesperson_id.name)
            print("Número de ofertas recibidas:", len(record.offer_ids))
            print("Mejor oferta recibida:", record.best_offer)
            if record.buyer_id:
                print("ID del comprador:", record.buyer_id.id)
                print("Nombre del comprador:", record.buyer_id.name)
            else:
                print("No hay comprador asociado a esta propiedad.")
            print("Tipo de propiedad:", record.property_type_id.name)
            print("Etiquetas asociadas:", record.tag_ids.mapped('name'))
            print("Precio esperado de la propiedad:", record.expected_price)
            print("Precio de venta de la propiedad:", record.selling_price)
            print("Estado de la propiedad:", record.state)
            print("Área total (habitable + jardín):", record.total_area)
            print("¿La propiedad tiene jardín?:", "Sí" if record.garden else "No")
            print("¿La propiedad tiene garaje?:", "Sí" if record.garage else "No")
            print("-" * 40)  # Separador para claridad