from odoo import fields, models, api
from odoo.exceptions import ValidationError

class InheritedModel(models.Model):
    _inherit = "estate.property"
    _description = "Inherited Model"

    move_type = fields.Selection(selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ], string='Type', store=True, index=True, tracking=True,
        default="entry", change_default=True)


    # @api.depends('offer_ids.price')
    def sold_property(self):
        print("hola")
        for r in self:
                    
            # Obtener la cuenta contable de ingresos por defecto
            account_id = self.env['account.account'].search([
                ('account_type', '=', 'income'),
                ('company_id', '=', self.env.company.id)
            ], limit=1).id
            
            if not account_id:
                raise ValidationError("No se encontró una cuenta de ingresos configurada")
            oferta = r.mapped('offer_ids.price')
            print(str(type(oferta)) + " : " + str(oferta))
            invoice_vals = {
                'partner_id': r.buyer_id.id,
                'move_type': r.move_type,
                # 'amount_untaxed_signed': oferta[0],
                # 'amount_total_signed': oferta[0] + 100 + (0.06 * oferta[0]),
                'invoice_date_due': fields.Date.today(),
                'property_id': r.id,
                'invoice_origin': r.name,
                'invoice_line_ids': [(0, 0, {
                    'name': 'Venta de propiedad ' + r.name,
                    'quantity': 1,
                    'price_unit': oferta[0],
                    'account_id': account_id,
                    'tax_ids': [(6, 0, [])],
                })],
            }
            invoice = self.env['account.move'].create(invoice_vals)
        return super().sold_property()