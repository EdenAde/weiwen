# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class ProjectProject(models.Model):

    _inherit = 'project.project'

    team_member_ids = fields.Many2many('res.users', 'project_user_rel', 'project_id',
                               'uid', 'Project Members', help="""Project's
                               members are users who can have an access to
                               the tasks related to this project.""",
                               states={'close':[('readonly',True)],
                                       'cancelled':[('readonly',True)]})
    team_id = fields.Many2one('project.team', string="Project Team")

    @api.onchange('team_id')
    def set_members_and_manager(self):
        self.update({'team_member_ids': [(6, 0, [rec.id for rec in self.team_id.team_member_ids])]})
        self.user_id = self.team_id.team_leader_id
