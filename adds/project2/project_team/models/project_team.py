# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class ProjectTeam(models.Model):
    _name = 'project.team'
    name = fields.Char(string="Name")
    code = fields.Char(string="Code")

    def _get_project_managers_domain(self):
        return [('groups_id', 'in', self.env.ref('project.group_project_manager').id)]
    team_leader_id = fields.Many2one('res.users', domain=_get_project_managers_domain, string="Team Leader")#, domain="[('id', 'in', team_member_ids)]")

    def _get_project_users_domain(self):
        return [('groups_id', 'in', self.env.ref('project.group_project_user').id)]
    team_member_ids = fields.Many2many('res.users', 'project_team_user_rel', 'team_id', 'uid', 'Project Members', domain=_get_project_users_domain)

    company_id = fields.Many2one('res.company', string="Company")
    active = fields.Boolean(string="Active", default=True)

    """@api.one
    @api.onchange('team_leader_id')
    def add_manager_to_team(self):
        if self.team_leader_id:
            if self.team_leader_id not in self.team_member_ids:
                members = []
                for m in self.team_member_ids:
                    members.append(m)
                members.append(self.team_leader_id)
                _logger.debug("Members : %s", members)
                
                #self.team_member_ids = [4, self.team_leader_id]
                self.update({'team_member_ids': [6, 0, members]})
    """
