# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from odoo import tools,fields,models,api
from odoo.osv import  osv

class book_report(models.Model):
    _name = "book.report"
    _description = "Book Statistics"
    _auto = False
    _rec_name = 'date'


    book_id=fields.Many2one('product.product', '书籍',readonly=True)
    pt_id=fields.Many2one('product.template', '书籍',readonly=True)
    cncateg = fields.Many2one('product.category', '中图分类', help="Select category for the current product")
    date=fields.Datetime('录入时间', readonly=True)
    school_id=fields.Many2one('school.school', '学校',readonly=True, domain="[('school_id', 'IS NOT', NULL)]")
    book_price=fields.Float(related="pt_id.list_price",string='价值', readonly=True,store=True)
    book_all=fields.Integer('总册数',group_operator="sum")
    book_sum=fields.Float('总值',group_operator="sum")
    #'pricelist_id': fields.many2one('product.pricelist', 'Pricelist', readonly=True),
    #'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True),
    #'section_id': fields.many2one('crm.case.section', 'Sales Team'),

    _order = 'date desc'

    def _select(self):
        select_str = """
             SELECT min(p.id) as id,
                    p.id as book_id,
                    p.school_id as school_id,
                    p.creation_date as date,
                    p.cncateg as cncateg,
                    count(*) as book_all,
                    pt.id as pt_id,
                    pt.list_price as book_price,
                    sum(pt.list_price) as book_sum
        """
        return select_str

    def _from(self):
        from_str = """
                product_product as p
                left join product_template pt on (p.product_tmpl_id=pt.id)
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY p.id,
                     pt.id,
                     p.school_id,
                     p.creation_date
                    
        """
        return group_by_str

    def _where(self):


        where_str = """
		        WHERE p.school_id IS NOT NULL
        """
        return where_str

    def _where2(self):
        where_str =""
        if(self.env.user.company_id.id>7):
            where_str = """
    		        AND p.school_id = %s 
                """ % self.env.user.company_id.school_id
        return where_str

    def _select2(self):
        return ''

    def _from2(self):
        return ''

    def _group_by2(self):
        return ''

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self._cr, self._table)
        dsql="""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            %s
            %s
            %s
            %s
            %s
            )""" % (self._table, self._select(), self._from(),self._where(),self._where2(), self._group_by(),self._select2(), self._from2(), self._group_by2())
        print(dsql)


        self._cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            %s
            %s
            %s
            %s
            %s
            )""" % (self._table, self._select(), self._from(),self._where(),self._where2(), self._group_by(),
                    self._select2(), self._from2(), self._group_by2()))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: