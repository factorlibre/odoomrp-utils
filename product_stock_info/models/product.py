# -*- coding: utf-8 -*-
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
from openerp import models
from openerp.osv import fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _product_available(self, cr, uid, ids, field_names=None, arg=False,
                           context=None):
        res = super(ProductProduct, self)._product_available(
            cr, uid, ids, field_names=field_names, arg=arg, context=context)
        for k, v in res.iteritems():
            res[k]['real_qty_available'] = (
                v['qty_available'] - v['outgoing_qty'])
        return res

    def _search_product_quantity(self, cr, uid, obj, name, domain, context):
        return super(ProductProduct, self)._search_product_quantity(
            cr, uid, obj, name, domain, context)

    _columns = {
        'qty_available': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Quantity On Hand',
            fnct_search=_search_product_quantity,
            help="Current quantity of products.\n"
            "In a context with a single Stock Location, this includes "
            "goods stored at this Location, or any of its children.\n"
            "In a context with a single Warehouse, this includes "
            "goods stored in the Stock Location of this Warehouse, or any "
            "of its children.\n"
            "stored in the Stock Location of the Warehouse of this Shop, "
            "or any of its children.\n"
            "Otherwise, this includes goods stored in any Stock Location "
            "with 'internal' type."),
        'virtual_available': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Forecast Quantity',
            fnct_search=_search_product_quantity,
            help="Forecast quantity (computed as Quantity On Hand "
            "- Outgoing + Incoming)\n"
            "In a context with a single Stock Location, this includes "
            "goods stored in this location, or any of its children.\n"
            "In a context with a single Warehouse, this includes "
            "goods stored in the Stock Location of this Warehouse, or any "
            "of its children.\n"
            "Otherwise, this includes goods stored in any Stock Location "
            "with 'internal' type."),
        'incoming_qty': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Incoming',
            fnct_search=_search_product_quantity,
            help="Quantity of products that are planned to arrive.\n"
            "In a context with a single Stock Location, this includes "
            "goods arriving to this Location, or any of its children.\n"
            "In a context with a single Warehouse, this includes "
            "goods arriving to the Stock Location of this Warehouse, or "
            "any of its children.\n"
            "Otherwise, this includes goods arriving to any Stock "
            "Location with 'internal' type."),
        'outgoing_qty': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Outgoing',
            fnct_search=_search_product_quantity,
            help="Quantity of products that are planned to leave.\n"
            "In a context with a single Stock Location, this includes "
            "goods leaving this Location, or any of its children.\n"
            "In a context with a single Warehouse, this includes "
            "goods leaving the Stock Location of this Warehouse, or "
            "any of its children.\n"
            "Otherwise, this includes goods leaving any Stock "
            "Location with 'internal' type."),
        'real_qty_available': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            fnct_search=_search_product_quantity,
            string='Available',)

    }


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _product_available(self, cr, uid, ids, field_names=None, arg=False,
                           context=None):
        res = super(ProductTemplate, self)._product_available(
            cr, uid, ids, field_names=field_names, arg=arg, context=context)
        for k, v in res.iteritems():
            res[k]['real_qty_available'] = (
                v['qty_available'] - v['outgoing_qty'])
        return res

    def _search_product_quantity(self, cr, uid, obj, name, domain, context):
        return super(ProductProduct, self)._search_product_quantity(
            cr, uid, obj, name, domain, context)

    _columns = {
        'qty_available': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Quantity On Hand',
            fnct_search=_search_product_quantity,
            help="Current quantity of products.\n"
            "In a context with a single Stock Location, this includes "
            "goods stored at this Location, or any of its children.\n"
            "In a context with a single Warehouse, this includes "
            "goods stored in the Stock Location of this Warehouse, or any "
            "of its children.\n"
            "stored in the Stock Location of the Warehouse of this Shop, "
            "or any of its children.\n"
            "Otherwise, this includes goods stored in any Stock Location "
            "with 'internal' type."),
        'virtual_available': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Forecast Quantity',
            fnct_search=_search_product_quantity,
            help="Forecast quantity (computed as Quantity On Hand "
            "- Outgoing + Incoming)\n"
            "In a context with a single Stock Location, this includes "
            "goods stored in this location, or any of its children.\n"
            "In a context with a single Warehouse, this includes "
            "goods stored in the Stock Location of this Warehouse, or any "
            "of its children.\n"
            "Otherwise, this includes goods stored in any Stock Location "
            "with 'internal' type."),
        'incoming_qty': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Incoming',
            fnct_search=_search_product_quantity,
            help="Quantity of products that are planned to arrive.\n"
            "In a context with a single Stock Location, this includes "
            "goods arriving to this Location, or any of its children.\n"
            "In a context with a single Warehouse, this includes "
            "goods arriving to the Stock Location of this Warehouse, or "
            "any of its children.\n"
            "Otherwise, this includes goods arriving to any Stock "
            "Location with 'internal' type."),
        'outgoing_qty': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            string='Outgoing',
            fnct_search=_search_product_quantity,
            help="Quantity of products that are planned to leave.\n"
            "In a context with a single Stock Location, this includes "
            "goods leaving this Location, or any of its children.\n"
            "In a context with a single Warehouse, this includes "
            "goods leaving the Stock Location of this Warehouse, or "
            "any of its children.\n"
            "Otherwise, this includes goods leaving any Stock "
            "Location with 'internal' type."),
        'real_qty_available': fields.function(
            _product_available, multi='qty_available',
            type='float',
            digits_compute=dp.get_precision('Product Unit of Measure'),
            fnct_search=_search_product_quantity,
            string='Available',)

    }
