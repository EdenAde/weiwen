# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api, _

class ProjectIssue(models.Model):
    _inherit = 'project.issue'

    team_member_ids = fields.Many2many('res.users', related='project_id.team_member_ids')