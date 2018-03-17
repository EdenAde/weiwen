# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class User(models.Model):
    _inherit = 'res.user'

    project_ids = ields.Many2many('project.project', 'project_team_user_rel',
                                    'team_id','uid', 'Project Members',
                                    help="""Project's members are users who
                                     can have an access to the tasks related
                                     to this project.""")
