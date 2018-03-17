# -*- coding: utf-8 -*-
import logging
from pyquery import PyQuery as pyq
_logger = logging.getLogger(__name__)
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#
from odoo import api,models,fields

import math

import time
import datetime

#from odoo.addons.web_socketio.namespace import OpenERPNameSpace

#from odoo.addons.web_socketio.web_socketio import SocketIO
from argparse import ArgumentParser


# class MyNameSpace(OpenERPNameSpace):
#
#     def on_myEvent(self):
#         print 'on_myEvent'
#         pass


class PosLibraryIssue(models.Model):
    _inherit = 'library.book.issue'

    school_id = fields.Many2one(related='card_id.student_id.school_id', string='学校',store=True,
                                states={'done': [('readonly', True)]})

    @api.model
    def create(self, vals):
        # When creating an expense product on the fly, you don't expect to
        # have taxes on it

        new_issue = super(PosLibraryIssue, self).create(vals)

        school_obj = self.env['school.school'].browse(new_issue.school_id.id)
        school_obj.write({'issue_amount':school_obj.issue_amount+1})
        #update_str = "update school_school set issue_amount=issue_amount+1   where id=%s" % (new_issue.school_id.id)
        print school_obj
        #self._cr.execute(update_str)

        return new_issue



class ReaderType(models.Model):

    _name = 'card.type'


    name=fields.Char('名称')
    book_limit=fields.Integer('允许借出本数')
    day_limit=fields.Integer('允许借出天数')
    book_day_rent=fields.Float('租金／天')
    overdur_rent = fields.Float('超期罚款／天')
    school_id = fields.Integer('学校', related='write_uid.company_id.school_id', store=False)






 # def get_default_day_to_return(self, fields):
 #        Param = self.env["ir.config_parameter"]
 #        return {
 #                'day_to_return': int(Param.get_param("day_to_return")),
 #                'book_limit': int(Param.get_param("book_limit")),
 #                }

class PosLibraryCard(models.Model):
    _inherit = 'library.card'

    @api.one
    @api.depends('type')
    def _get_book_limit_f(self):
        #self.book_limit_f = self.book_limit or self.type_book_limit or self.env["ir.config_parameter"].get_param('book_limit')
        self.book_limit_f = self.type.book_limit

    @api.one
    @api.depends('type')
    def _get_day_limit_f(self):
        #self.day_limit_f = self.day_limit or self.type_day_limit or self.env["ir.config_parameter"].get_param('day_to_return')
        self.day_limit_f = self.type.day_limit



    @api.one
    def _get_user_barcode(self):
        if self.student_id:
            self.user_barcode = self.student_id.barcode
        if self.teacher_id:
            self.user_barcode = self.teacher_id.barcode

    @api.one
    @api.onchange('teacher_id','student_id')
    def _set_user_barcode(self):
        pass
        # if self.student_id:
        #     self.student_id.barcode = self.user_barcode
        # if self.teacher_id:
        #     self.teacher_id.barcode = self.user_barcode

    @api.model
    def create(self, vals):
        # When creating an expense product on the fly, you don't expect to
        # have taxes on it
        print "default_card_type"
        print not vals.get('type')
        if not vals.get('type'):
            #
            default_card_type = self.env['card.type'].search([('name','=','hyq_default_card_type')])
            print default_card_type
            if not default_card_type:

                vals['type']=13

        vals['school_id'] = self.env.user.company_id.school_id

        newcard = super(PosLibraryCard, self).create(vals)
        #self._cr.commit()
        if newcard.student_id:
            # print "newcard"
            # print newcard
            newcard.student_id.user_id.write({'card_id':newcard.id})
        elif newcard.teacher_id:
            self.env['res.partner'].search([('barcode','=',newcard.code)]).write({'card_id':newcard.id})
            #newcard.teacher_id.partner_id.user_id.write({'card_id':newcard.id})
        return newcard

    # @api.model
    # def create(self, vals):
    #     print ('post_method')
    #     stu = self.env['student.student'].browse(vals)
    #     print stu
    #     for st in stu:
    #         # print st
    #         if self.student_id:
    #             st.user_id.write({'card_id': st.card_id.id, 'company_id': self.env.user.company_id.id})
    #         st.card_id.sudo().write({'student_id': st.id})
    #             student_id.user_id.write({'card_id': st.card_id.id})
    @api.one
    def _get_school(self):
        if self.student_id  and self.student_id.school_id:
            print "self.student_id.school_id.id"
            print self.student_id.school_id.id
            self.school_id = self.student_id.school_id.id
        elif self.teacher_id  and self.teacher_id.school:
            print "self.teacher_id.school.id"
            print self.teacher_id.school.id
            self.school_id = self.teacher_id.school.id
        else:
            self.school_id = 0

    @api.one
    @api.depends('student_id','teacher_id')
    def _set_school_id(self,value):
        self.school_id=value



    @api.model
    def set_reader_school(self):

        sql = "select id from library_card "

        self._cr.execute(sql)
        ids =[row[0] for row in self._cr.fetchall()]
        print ids
        card_objs = self.browse(ids)
        print card_objs
        for reader in card_objs:
            school_id=0
            if reader.student_id:
                school_id=reader.student_id.school_id.id
            elif reader.teacher_id:
                school_id = reader.teacher_id.school.id
            if school_id:
                sql = "update library_card set school_id=%s where id=%s" % (school_id,reader.id)
                self._cr.execute(sql)
            #reader.write({'school_id':school_id})



    @api.one
    def _set_book_limit(self,value):
        self.book_limit = value

    @api.one
    def _set_day_limit(self, value):
        self.day_limit = value



    school_id = fields.Integer('学校',store=True)
    issue_all_ids = fields.One2many('library.book.issue', 'card_id', string='issues')
    day_limit = fields.Integer('类型允许借出天数')
    type = fields.Many2one('card.type')
    type_book_limit=fields.Integer('类型允许借出本数',related='type.book_limit')
    type_day_limit = fields.Integer('类型允许借出天数', related='type.day_limit')

    book_limit_f = fields.Integer('允许借出本数', compute='_get_book_limit_f',inverse='_set_book_limit',store=True)
    day_limit_f = fields.Integer('允许借出天数', compute='_get_day_limit_f',inverse='_set_day_limit_',store=True)
    user_barcode = fields.Char('所属人编号',compute="_get_user_barcode",inverse='_set_user_barcode',store=True)



    _defaults = {
        'book_limit_f': 5,
        'day_limit_f':7
    }

class PosLibraryStudent(models.Model):
    _inherit = 'student.student'

    quantity = fields.Integer("数量")

    cmp_id = fields.Many2one('res.company', string="Company Name",
                             related='school_id.company_id', store=True)
    school_id = fields.Many2one('school.school', '学校',
                                states={'done': [('readonly', True)]})
    card_id = fields.Many2one('library.card',string='借书证')
    issue_all_ids = fields.One2many('library.book.issue', 'card_id', string='Name', ondelete='cascade')


    @api.model
    def onchange_pid(self,val):
        res = {}
        res.setdefault('value', {})
        print "antoine@openerp.comantoine@openerp.comantoine@openerp.comantoine@openerp.comantoine@openerp.com"
        res['value']['school_id']=self.env.user.company_id.school_id
        res['value']['country_id'] = self.env.user.company_id.country_id
        res['value']['state_id'] = self.env.user.company_id.state_id
        res['value']['city_id'] = self.env.user.company_id.city_id

        res['value']['county'] = self.env.user.company_id.county
        res['value']['town'] = self.env.user.company_id.town

        return res





    @api.model
    def update_card(self,vals):
        print ('post_method')
        stu = self.env['student.student'].browse(vals)
        print stu
        for st in stu:
            #print st
            st.user_id.write({'card_id':st.card_id.id,'company_id':self.env.user.company_id.id})
            st.card_id.sudo().write({'student_id': st.id})
            st.user_id.write({'card_id':st.card_id.id})
        # if stus.ensure_one:
        #     for stu in stus:
        #         self.env['library.card'].browse(stu.card_id).write({'student_id':stu.id})
        # else:
        #     stus



    @api.model
    def create(self, vals):
        # When creating an expense product on the fly, you don't expect to
        # have taxes on it
        vals['is_student']=True
        newstudent  =super(PosLibraryStudent, self).create(vals)
        _logger.info("start_to_up_stu_count")
        school_obj = self.env['school.school'].browse(newstudent.school_id.id)
        school_obj.write({'student_amount': school_obj.student_amount + 1})
        _logger.info("start_to_up_stu_count_after")
        #update_str = "update school_school set student_amount=student_amount+1   where id=%s" % (newstudent.school_id.id)
        #self._cr.execute(update_str)

        return newstudent

    _defaults = {
        'quantity': 1,
        'date_of_birth':lambda :datetime.now(),
    }



class PosLibrarySchoolDevision(models.Model):
    _name = 'school.school.division'


    name=fields.Char("名称")


class PosLibrarySchool(models.Model):
    _inherit = 'school.school'

    def run(self):
        parser = ArgumentParser(description='Gevent WSGI server')
        parser.add_argument('-d', dest='db', default='hyqeducation',
                            help="'list of db names, separated by ','")
        parser.add_argument('-i', dest='interface', default='127.0.0.1',
                            help="Define the interface to listen")
        parser.add_argument('-p', dest='port', default=8068,
                            help="Define the port to listen")
        parser.add_argument('-c', dest='config_file', default='',
                            help="Config file of openerp use for addons_path")
        parser.add_argument('--max-cursor', dest='maxcursor', default=2,
                            help="Max declaration of cursor by data base")
        # parser.add_argument('--load-language', dest='load_language', default='',
        #                     help="")

        # args = parser.parse_args()
        # socketio = SocketIO(args)
        # socketio.serve_forever()

        #SocketIO.add_namespace('/mynamespace', MyNameSpace)
        return

    @api.model
    def create(self, vals):
        # When creating an expense product on the fly, you don't expect to
        # have taxes on it

        new_school = super(PosLibrarySchool, self).create(vals)
        _logger.info(new_school.company_id.school_id)
        _logger.info(new_school.company_id)
        new_school.company_id.school_id = new_school.id
        return new_school
        # sid = new_school.id
        # self.env['res.company'].browse(new_school.company_id.id)
        # new_school.company_id.update({
        #     'school_id':sid
        # })


    @api.one
    def _get_student_amount(self):
        try:
            select_str = "select count(*) as bon from student_student where school_id=%s" % (self.id)
            _logger.info(select_str)
            self.env.cr.execute(select_str)
            res = self.env.cr.fetchone()
            # print int(res[0])
            self.student_amount = int(res[0])
        except Exception as e:
            pass



    @api.multi
    def udate_school(self):
        for school in self:
            print "school"
            print school
            school.company_id.write({"school_id":school.id})

        sql = "select distinct(id)  from school_school"
        self._cr.execute(sql)
        schools = self._cr.fetchall()

        print "schools="
        print schools


        for (next_sequence,) in schools:
            school = self.browse(next_sequence)
            school.company_id.write({"school_id":school.id})

    @api.one
    def _get_issue_amount(self):
        select_str = "select count(id) as bon from library_book_issue where school_id=%s" % (self.id)
        self.env.cr.execute(select_str)
        res = self.env.cr.fetchone()
        self.issue_amount = int(res[0])

    @api.one
    def _get_book_amount(self):
        try:
            select_str = "select count(id) as bon from product_product where school_id=%s" % (self.id)
            _logger.info(select_str)
            self.env.cr.execute(select_str)
            res = self.env.cr.fetchone()
            # print int(res[0])
            self.book_amount = int(res[0])
        except Exception as e:
            pass

    @api.multi
    @api.depends('student_amount','book_amount')
    def _get_avg_book(self):

        for rec in self:
            if rec.student_amount>0:
                rec.avg_book =  math.floor(rec.book_amount/rec.student_amount)


    @api.one
    @api.depends('student_amount','issue_amount')
    def _get_avg_borrow_book(self):
        print "self.student_amount"
        print self.student_amount
        if self.student_amount>0:
            self.avg_borrow_book =  round(self.issue_amount/float(self.student_amount),4)*100

    @api.one
    @api.depends('book_amount','issue_amount')
    def _get_avg_issue(self):
        if self.book_amount>0:
            self.avg_issue =  round(self.issue_amount/float(self.book_amount))*100





    school_latitude_longitude = fields.Char("经纬度")
    school_sort = fields.Integer('排序')
    school_latitude = fields.Char("经度")
    school_longitude = fields.Char("纬度")
    student_count = fields.Integer("学生总数")
    issue_amount = fields.Integer('流通总数', help="流通总数")
    student_amount = fields.Integer('读者总数', help="读者总数")
    book_amount = fields.Integer('书籍总数', help="书籍总数")
    division = fields.Selection([("小学", '小学'),
                                 ("中学", '中学'), ("九年一贯", '九年一贯')],
                                '学部', help="Select division"
                                )
    division_name = fields.Many2one('school.school.division',string='学部')

    division_name_name=fields.Char(related='division_name.name',string="学部",store=True)

    avg_book = fields.Integer("生均册数",compute='_get_avg_book',store=True)
    avg_borrow_book = fields.Float("借阅率",compute='_get_avg_borrow_book',store=True)
    avg_issue = fields.Float(compute='_get_avg_issue',store=True,sting='流通率')

    town_name=fields.Char('town name',related='company_id.town.name',store=True)

    user_id = fields.Many2one('res.users',string="管理员")


    defaults = {
        division: "小学"
    }



