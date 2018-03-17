# -*- coding: utf-8 -*-
# Copyright 2012, Israel Cruz Argil, Argil Consulting
# Copyright 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class TmsEvent(models.Model):
    _name = "tms.event"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Events"
    _order = "date"

    name = fields.Char(
        string='Description', required=True)
    state = fields.Selection(
        [('draft', '草稿'),
         ('confirm', '确认'),
         ('cancel', '取消')], readonly=True, default='draft')
    date = fields.Date(
        default=fields.Date.context_today,
        required=True,
        states={'confirmed': [('readonly', True)],
                'cancel': [('readonly', True)]})
    notes = fields.Text(
        states={'confirmed': [('readonly', True)],
                'cancel': [('readonly', True)]})
    travel_id = fields.Many2one(
        'tms.travel', '出差', index=True, required=True, readonly=False,
        states={'confirmed': [('readonly', True)],
                'cancel': [('readonly', True)]}, ondelete='restrict')
    latitude = fields.Float(
        states={'confirmed': [('readonly', True)],
                'cancel': [('readonly', True)]})
    longitude = fields.Float(
        states={'confirmed': [('readonly', True)],
                'cancel': [('readonly', True)]})
    position_real = fields.Text(
        help="GPS",
        states={'confirmed': [('readonly', True)],
                'cancel': [('readonly', True)]})
    position_pi = fields.Text(
        string='地址',
        states={'confirmed': [('readonly', True)],
                'cancel': [('readonly', True)]})

    attachments = fields.One2many('ir.attachment','res_id','附件')

    @api.multi
    def action_confirm(self):
        for rec in self:
            rec.message_post(body=_('<b>确认.</b>'))
            rec.state = 'confirm'

    @api.multi
    def action_cancel(self):
        for rec in self:
            rec.message_post(body=_('<b>取消.</b>'))
            rec.state = 'cancel'

    @api.multi
    def set_2_draft(self):
        for rec in self:
            rec.message_post(body=_('<b>Event Draft.</b>'))
            rec.state = 'draft'
