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
import re


class ea_import_template_line_boolean_field(models.Model):
    _name = 'ea_import.template.line.boolean_field'

    regexp=fields.Char('Regexp', size=512, help='Python Search Regular Expresiion', required="1")
    template_line_id=fields.Many2one('ea_import.template.line', 'Template Line',)
    boolean_value=fields.Boolean('Boolean Value', )


    @api.multi
    def get_value(self,target_string):
        for boolean_field in self:
            search_result = re.search(boolean_field.regexp, target_string)
            if search_result:
                return boolean_field.boolean_value
        return False




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
