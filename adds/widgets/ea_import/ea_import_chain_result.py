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
from odoo import fields,api,models
import base64


class ea_import_chain_result(models.Model):
    _name = 'ea_import.chain.result'
    _order = 'import_time desc'

    name = fields.Char('Model', size=256, required=True)
    chain_id = fields.Many2one('ea_import.chain',)  # to be removed
    log_id = fields.Many2one('ea_import.log',)
    result_ids_file = fields.Binary('Result Ids',)
    import_time = fields.Datetime('Import Time',)
    scheduler_log_id = fields.Many2one('ea_import.scheduler.log', 'Scheduler Log')


    _defaults = {
    }

    @api.multi
    def show_result(self):
        for result in self:
            result_ids = eval(base64.b64decode(result.result_ids_file))
            return {
                'name': 'Result',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'view_id': False,
                'res_model': result.name,
                'domain': [('id', 'in', result_ids)],
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
            }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
