# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Daniel Reis
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

#from openerp.osv import fields, orm,modules
from odoo import models, fields, api, _,modules


from odoo import tools




class blogaseModel(models.Model):
    _inherit = 'blog.post'

    def _default_image(self):
        image_path = modules.get_module_resource('im_livechat', 'static/src/img', 'default.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    sequence = fields.Integer(
        '序号',
        help=("Gives the sequence order when displaying "
              "a list of contexts."))

    image = fields.Binary("Photo", default=_default_image, attachment=True,
                          help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True,
                                 help="Medium-sized photo of the employee. It is automatically "
                                      "resized as a 128x128px image, with aspect ratio preserved. "
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized photo", attachment=True,
                                help="Small-sized photo of the employee. It is automatically "
                                     "resized as a 64x64px image, with aspect ratio preserved. "
                                     "Use this field anywhere a small image is required.")

    _defaults = {
        'sequence': 1
    }



class ProjectReport(models.Model):
    ''' Defining a teacher information '''
    _name = 'project.report'

    p_id = fields.Many2one('project.project','xiangmu', select=True)
    user_id = fields.Many2one(
        'res.users', 'baogaoren',select=True)

    des = fields.Char('miaoshu')
    #
    report_stage_name = fields.Char(string='jieduan')
    #
    report_name = fields.Char(string='jieduan')



class ProjectBids(models.Model):
    _name = 'project.bid'


    p_id= fields.Many2one('project.project', 'xiangmu', select=True)
    price=fields.Float('jiage', size=10)
    user_id=fields.Many2one(
            'res.users', 'toubiaoren', select=True)
    des=fields.Char('miaoshu')

    state=fields.Selection([
        ('1', '中标'),
        ('2', '无'),
        ], string='中标状态', required=True, default='1')


class ProjectProject(models.Model):
    _inherit = 'project.project'

    #bis_ids = fields.One2many('project.bid','p_id', string='baojia')
    report_id = fields.Many2one('project.report', 'baogao')
    zipin = fields.Boolean('自评')



    @api.model
    def copy_project(self,vals):
        return self.copy_data(vals)


class TaskAnalytic(models.Model):
    _inherit = 'project.project'

    #bis_ids = fields.One2many('project.bid','p_id', string='baojia')
    report_id = fields.Many2one('project.report', 'baogao')
    zipin = fields.Boolean('自评')



    @api.model
    def copy_project(self,vals):
        return self.copy_data(vals)


class resPartner(models.Model):
    _inherit = 'res.users'

    #bis_ids = fields.One2many('project.bid','p_id', string='baojia')
    user_type = fields.Selection([('1', '公众'), ('2', '专家'), ('3', '专业机构'), ('4', '第三方服务公司'), ('6', '单位')], default='1')
