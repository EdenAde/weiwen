from odoo import http
from odoo.http import request

class vit_website(http.Controller):

	@http.route('/partner/list', type='http', auth="public", website=True)
	def list(self, **kw):
		partner=request.env['res.partner'].search([])
		data = {
			'partner' : partner
		}
		return request.render('vit_web_partner.list', data)