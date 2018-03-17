# -*- encoding: utf-8 -*-

__author__ = 'vincent'

import logging

from openerp import models
from openerp.addons.base.ir import ir_qweb

logger = logging.getLogger(__name__)

class Map(models.AbstractModel):
	_name = 'website.qweb.field.map'
	_inherit = ['ir.qweb.field.many2one']

	def record_to_html(self, cr, uid, field_name, record, options=None, context=None):
		if options is None:
			options = {}
		fields = options.get('fields') or ["longitude", "latitude"]

		if context is None:
			context = {}

		value_rec = record[field_name]
		if not value_rec:
			return None
		value_rec = value_rec.sudo().with_context(show_map=True)

		val = {
			'longitude': value_rec.longitude,
			'latitude': value_rec.latitude,
			'fields': fields,
			'object': value_rec,
			'options': options
		}

		html = self.pool["ir.ui.view"].render(cr, uid, "odoo_extension.map", val, engine='ir.qweb', context=context).decode('utf8')

		return ir_qweb.HTMLSafe(html)

class Map2(models.AbstractModel):
	_name = 'ir.qweb.widget.map'
	_inherit = 'ir.qweb.field'

	def _format(self, inner, options, qwebcontext):
		engine = self.pool["ir.qweb"]
		object = engine.eval(inner, qwebcontext)
		fields = options['fields']

		val = {
			'longitude': object[fields[0]],
			'latitude': object[fields[1]],
			'fields': fields,
			'object': object,
			'options': options
		}
		qwebcontext.update(val)

		html = engine.render(object.env.cr, object.env.uid, "odoo_extension.map", qwebcontext=qwebcontext, context=val).decode('utf8')

		return ir_qweb.HTMLSafe(html)