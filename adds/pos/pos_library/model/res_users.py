# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)
class ResUsers(models.Model):
    _inherit = 'res.users'



    @api.model
    def update_card(self,vals):
        print ('post_method')
        stu = self.env['student.student'].browse(vals)
        for st in stu:
            #print st
            st.user_id.write({'card_id':st.card_id.id,'company_id':self.env.user.company_id.id})
            st.card_id.sudo().write({'student_id': st.id})
            st.user_id.write({'card_id':st.card_id.id})

    @api.model
    def update_role(self):

        sql = "select * from res_users"
        self._cr.execute(sql)
        users = self._cr.dictfetchall()

        _logger.info(users)
        for user in users:
            print user['id']

            #stu = self.env['student.student'].search([('user_id', '=', user['id'])])
            sql2 = "select * from student_student where user_id=%s" % user['id']
            self._cr.execute(sql2)
            res = self._cr.fetchall()
            #print res
            if res:
                sql3 = "update res_users set is_student = True where id=%s " % user['id']
                self._cr.execute(sql3)
                self._cr.commit()



    # @api.one
    # def _is_student(self):
    #     stu = self.env['student.student'].search([('user_id','=',self.id)])
    #     print stu
    #     if stu:
    #         self.is_student=True
    #     else:
    #         self.is_student = False




    # @api.one
    # def _set_is_student(self,value):
    #     self.is_student=value



    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        #print "self.env.user.company_id.id"
        #print self.env.user.company_id.id
        if self.env.user.company_id.id!=1 and self._context.get('myschool'):
            args += [('company_id', 'child_of', [self.env.user.company_id.id])]

        return super(ResUsers, self).search(args, offset, limit, order, count)





    is_student = fields.Boolean('学生用户')
    is_teacher=fields.Boolean('教师用户')

