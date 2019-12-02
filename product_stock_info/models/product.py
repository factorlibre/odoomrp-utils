##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 FactorLibre (<http://www.factorlibre.com>).
#    @author Ismael Calvo <ismael.calvo@factorlibre.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import openerp.addons.decimal_precision as dp
from openerp.addons.stock.models.product import OPERATORS
from odoo.exceptions import UserError
from openerp import api, models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _compute_real_qty(self):
        res = self._compute_real_qty_dict(
            self._context.get('lot_id'), self._context.get('owner_id'),
            self._context.get('package_id'), self._context.get('from_date'),
            self._context.get('to_date'))

        for product in self:
            product.real_qty_available = res[product.id]['real_qty_available']

    def _compute_real_qty_dict(self, lot_id, owner_id, package_id,
                               from_date=False, to_date=False):
        res = self._compute_quantities_dict(
            lot_id, owner_id, package_id, from_date=from_date, to_date=to_date)

        for product in self.with_context(prefetch_fields=False):
            res[product.id]['real_qty_available'] = (
                res[product.id]['qty_available'] -
                res[product.id]['outgoing_qty'])

        return res

    def _search_real_qty_available(self, operator, value):
        return self._search_product_real_quantity(
            operator, value, 'real_qty_available')

    def _search_product_real_quantity(self, operator, value, field):
        if field not in ('real_qty_available'):
            raise UserError(('Invalid domain left operand %s') % field)
        if operator not in ('<', '>', '=', '!=', '<=', '>='):
            raise UserError(('Invalid domain operator %s') % operator)
        if not isinstance(value, (float, int)):
            raise UserError(('Invalid domain right operand %s') % value)

        ids = []
        for product in self.search([]):
            if OPERATORS[operator](product[field], value):
                ids.append(product.id)
        return [('id', 'in', ids)]

    real_qty_available = fields.Float(
        string='Available',
        digits=dp.get_precision('Product Unit of Measure'),
        search='_search_real_qty_available',
        compute='_compute_real_qty')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _compute_real_qty(self):
        res = self._compute_real_qty_dict()

        for template in self:
            template.real_qty_available = res[template.id][
                'real_qty_available']

    def _compute_real_qty_dict(self):
        res = self._compute_quantities_dict()

        for template in self:
            res[template.id]['real_qty_available'] = (
                res[template.id]['qty_available'] -
                res[template.id]['outgoing_qty'])

        return res

    def _search_real_qty_available(self, operator, value):
        domain = [('real_qty_available', operator, value)]
        product_variant_ids = self.env['product.product'].search(domain)
        return [('product_variant_ids', 'in', product_variant_ids.ids)]

    real_qty_available = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'),
        search='_search_real_qty_available',
        compute='_compute_real_qty',
        string='Available',)
