# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 ENNAPS LTD (<http://www.enapps.co.uk>).
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


class import_wizard(models.TransientModel):

    _name = 'import.wizard'
    _description = 'Simple import wizard'

    chain_id = fields.Many2one('ea_import.chain', '导入链', )
    import_file=fields.Binary('导入文件', )
    type = fields.Selection([
                            ('csv', 'CSV 导入'),
                            ('ftp', 'ftp '),
                            ('mysql', 'MySql 导入'),
                            ('xls', 'xls 导入'),
                            ], '导入类型',
                            default='csv',
                            required=True,
                            readonly=True,
                            help="Type of connection import will be done from")


    _defaults = {
         'chain_id': lambda self: self.env.context.get('import_chain_id'),
         'type': lambda self: self.env.context.get('import_chain_id') and self.pool.get('ea_import.chain').browse(self.env.context['import_chain_id']).type or 'csv',
    }

    @api.multi
    def do_import(self):
        for wizard in self:
            wizard.chain_id.write({'input_file': wizard.import_file})
            print wizard.chain_id.id
            self._cr.commit()
            wizard.chain_id.with_context(import_chain_id=wizard.chain_id.id).import_to_db()
        return {'type': 'ir.actions.act_window_close'}

#import_wizard()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
