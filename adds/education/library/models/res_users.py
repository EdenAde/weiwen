# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    pos_config=fields.Many2one('pos.config', '终端')





