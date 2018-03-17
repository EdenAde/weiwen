# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Enapps LTD (<http://www.enapps.co.uk>).
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

from odoo.osv import osv
from odoo import fields,models,api


class ea_import_log(models.Model):
    _name = 'ea_import.log'
    _order = 'import_time desc'

    log_line=fields.One2many('ea_import.log.line', 'log_id', 'Log Line')
    import_time=fields.Datetime('Import Time',)
    chain_id=fields.Many2one('ea_import.chain', 'Import Chain')
    result_ids=fields.One2many('ea_import.chain.result', 'log_id', 'Import Results', )




class ea_import_log_line(models.Model):
    _name = 'ea_import.log.line'
    name = fields.Char('Log', size=516,)
    log_id = fields.Many2one('ea_import.log', 'Log ID', readonly=True)

