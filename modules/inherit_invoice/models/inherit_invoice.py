import logging
from odoo import models, api, exceptions, _

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _check_edit_restriction(self, vals_list):
        print("Entro en _check_edit_restriction")
        for line, vals in zip(self, vals_list):
            move = None
            # Caso create: si viene el move_id en vals
            if vals.get('move_id'):
                move = self.env['account.move'].browse(vals['move_id'])
            # Caso write: usar el move_id del record ya existente
            elif line and line.move_id:
                move = line.move_id

            _logger.warning("Intento de edición en factura ligada a SO: %s", self.env.user.has_group('inherit_invoice.invoice_inherit_group_invoice_edit_sale_linked'))
            if move and move.invoice_origin and not self.env.user.has_group('inherit_invoice.invoice_inherit_group_invoice_edit_sale_linked'):
                _logger.warning("Intento de edición en factura ligada a SO: %s", move.name)
                _logger.warning("Intento de edición en factura ligada a SO: %s", self.env.user.name)
                _logger.warning("move invoice: %s", move.invoice_origin)
                raise exceptions.UserError(
                    _("No puedes modificar líneas de facturas que provienen de pedidos de venta.")
                )

    # @api.model
    def create(self, vals_list):
        print("Entro en create")
        records = super().create(vals_list)
        records._check_edit_restriction(vals_list)
        return records

    def write(self, vals):
        print("Entro en write")
        res = super().write(vals)
        self._check_edit_restriction([vals] * len(self))
        return res
