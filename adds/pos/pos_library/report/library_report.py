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

class library_report(models.Model):
    _name = "library.report"
    _description = "library Orders Statistics"
    _auto = False
    _rec_name = 'date'

    date=fields.Datetime('借书时间', readonly=True)  # TDE FIXME master: rename into date_order
    date_return=fields.Datetime('还书时间', readonly=True)
    actual_return_date=fields.Datetime('实际还书时间', readonly=True)
        #'issue_id': fields.many2one('library.book.issue', '流通', readonly=True),
        #'product_uom': fields.many2one('product.uom', 'Unit of Measure', readonly=True),
        #'product_uom_qty': fields.float('# of Qty', readonly=True),
    reader_id=fields.Many2one('student.student', '学生',readonly=True)

    book_id=fields.Many2one('product.product', '书籍',readonly=True)
    school_id=fields.Many2one('school.school', '学校',readonly=True)
    standard_id = fields.Many2one('school.standard',  string='班级')
    standard_d_id = fields.Many2one('standard.standard', string='年级')
        #'user_id': fields.many2one('res.users', 'Salesperson', readonly=True),
        #'price_total': fields.float('Total Price', readonly=True),
        #'delay': fields.float('Commitment Delay', digits=(16,2), readonly=True),
    categ_id=fields.Many2one('product.category',u'中图分类', readonly=True)

    nbr=fields.Integer('#共计（本）', readonly=True,group_operator="sum")
    # TDE FIXME master: rename into nbr_lines
    user_id = fields.Many2one('res.users','图书管理员')
    #nbrm=fields.Float('#共计（元）', readonly=True)  # TDE FIXME master: rename into nbr_lines
    state=fields.Selection([
            ('draft', '借出'),
            ('issue', '借出'),
            ('return', '归还'),
            ('lost', '丢失'),
            ], '借书状态', readonly=True)
        #'pricelist_id': fields.many2one('product.pricelist', 'Pricelist', readonly=True),
        #'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True),
        #'section_id': fields.many2one('crm.case.section', 'Sales Team'),                    (select count(*)/(select  count(*) from product_product where product_product.school_id=l.school_id) as avg_issue),
    _order = 'date desc'

    def _select(self):
        select_str = """
             SELECT min(l.id) as id,
                    p.id as book_id,
                    sc.id as school_id,
                    l.state as state,
                    l.student_id as reader_id,
                    stu.standard_id as standard_id,
                    sst.standard_id as standard_d_id,
                    l.actual_return_date as actual_return_date,
                    l.date_return as date_return,
                    l.date_issue as date,
                    count(*) as nbr,
                    p.cncateg as categ_id,
                    users.id as user_id,
                    case when sc.book_amount =0 then 0 else count(*)* 1000.0 /sc.book_amount end as avg_issue
        """
        return select_str

    def _from(self):
        from_str = """
                library_book_issue l
                left join product_product p on (l.name=p.id)
                left join school_school sc on (l.school_id=sc.id)
                left join res_users users on (sc.user_id=users.id)
                left join product_category c on (p.cncateg=c.id)
                left join student_student stu on (l.student_id=stu.id)
                left join school_standard sst on stu.standard_id = sst.id
                left join standard_standard ssd on sst.standard_id = ssd.id

        """
        return from_str

    def _where(self):
        where_str = """
           
        """
        return where_str

    def _group_by(self):
        group_by_str = """
            GROUP BY p.cncateg,
                    sc.id,
                    p.id,
                    l.state,
                    l.date_return,
                    l.date_issue,
                    l.actual_return_date,
                    l.student_id,
                    stu.standard_id,
                    sst.standard_id,
                    users.id
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
            )""" % (self._table, self._select(), self._from(), self._where(),self._group_by(),self._select2(), self._from2(), self._group_by2())
        print(dsql)


        self._cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            %s
            %s
            %s
            %s
            )""" % (self._table, self._select(), self._from(), self._where(), self._group_by(),
                    self._select2(), self._from2(), self._group_by2()))
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: