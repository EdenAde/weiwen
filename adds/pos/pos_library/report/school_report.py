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

class school_report(models.Model):
    _name = "school.report"
    _description = "School Statistics"
    _auto = False

    #book_id = fields.Many2one('product.product', '书籍',readonly=True)



    name = fields.Char('学校', readonly=True)

    division_name = fields.Char('学部', readonly=True)

    town_name = fields.Char('乡镇')

    book_all=fields.Integer('藏书量（册）')

    issue_all = fields.Integer('流通总量')

    student_all=fields.Integer('读者总数（人）')

    avg_book=fields.Integer('生均册数（册）',readonly=True,group_operator="avg")

    avg_borrow_book=fields.Float('借阅率（%）',readonly=True,group_operator="avg")

    avg_issue=fields.Float('流通率（%）',readonly=True,group_operator="avg")

    school_sort = fields.Integer('排序')


    # TDE FIXME master: rename into nbr_lines

        #'reader_sum':fields.integer('学生总数',readonly=True),
        # 'avg_books':fields.float('藏书利用率',readonly=True),
        # 'avg_reader':fields.float('读者借阅率',readonly=True),
        #'avg_issue':fields.float('图书流通率',readonly=True),
        #'pricelist_id': fields.many2one('product.pricelist', 'Pricelist', readonly=True),
        #'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True),
        #'section_id': fields.many2one('crm.case.section', 'Sales Team'),

    _order = 'school_sort desc'

    def _select(self):
        select_str = """
            SELECT min(com.id) as id,
                    p.com_name as name,
                    p.division_name_name as division_name,
                    p.town_name as town_name,
                    p.school_sort as school_sort,
                    p.issue_amount as issue_all,
                    p.student_amount as student_all,
                    p.book_amount as book_all,
                    p.avg_book as avg_book,
                    p.avg_borrow_book as avg_borrow_book,
                    p.avg_issue as avg_issue
        """
        return select_str

    def _from(self):
        from_str = """
            school_school as p left join res_company as com on p.company_id = com.id
        """
        return from_str

    def _where(self):
        where_str = """
        """
        return where_str


    def _group_by(self):
        group_by_str = """
        GROUP BY  p.com_name,
        p.division_name_name,
        p.school_sort,
        p.issue_amount,
        p.student_amount,
        p.book_amount,
        p.avg_book,
        p.avg_borrow_book,
        p.avg_issue,
        p.town_name
        """
        return group_by_str

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
            )""" % (self._table, self._select(), self._from(),self._where(), self._group_by(),self._select2(), self._from2(), self._group_by2())
        print(dsql)


        self._cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            %s
            %s
            %s
            %s
            )""" % (self._table, self._select(), self._from(),self._where(), self._group_by(),
                    self._select2(), self._from2(), self._group_by2()))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: