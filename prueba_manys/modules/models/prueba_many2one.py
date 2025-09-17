from odoo import fields, models

class prueba_many2one(models.Model):
    _name = "prueba.many2one"
    _description = "Prueba Many2one"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripcion")

    property_id = fields.Many2one(
        'estate.property',
        string="Propiedad",
        required=True
    )
    