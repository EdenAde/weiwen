# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _

import logging
_logger = logging.getLogger(__name__)
    
    
class ResPartner(models.Model):
    _inherit = 'project.project'

    task_planned_hours_sum = fields.Float(string="Planned Hours Sum for Tasks", compute='_compute_task_planned_hours_sum')
    task_effective_hours_sum = fields.Float(string="Effective Hours Sum for Tasks", compute='_compute_task_effective_hours_sum')
    issue_effective_hours_sum = fields.Float(string="Effective Hours Sum for Issues", compute='_compute_issues_effective_hours_sum')
    total_effective_hours_sum = fields.Float(string="Total effective Hours Sum", compute='_compute_total_effective_hours_sum')
    total_timesheets_hours_sum = fields.Float(string="Total Timesheets Hours Sum", compute='_compute_total_timesheets_hours_sum')
    total_difference_estimation_effective_sum = fields.Float(string="Total difference between estimation and effective", compute='_compute_total_difference_estimation_effective_sum')
    total_timesheets_not_linked_sum = fields.Float(string="Total timesheets not linked to task or issue", compute='_compute_total_timesheets_not_linked_sum')
    
    @api.one
    def _compute_task_planned_hours_sum(self):
        self.task_planned_hours_sum = sum([task.planned_hours for task in self.task_ids])
    
    @api.one
    def _compute_task_effective_hours_sum(self):
        self.task_effective_hours_sum = sum([task.effective_hours for task in self.task_ids])

    @api.one
    def _compute_issues_effective_hours_sum(self):
        issues_sum = 0
        for issue in self.issues:
            issues_sum = issues_sum + sum([timesheet.unit_amount for timesheet in issue.timesheet_ids])
        self.issue_effective_hours_sum = issues_sum

    @api.one
    def _compute_total_effective_hours_sum(self):
        self.total_effective_hours_sum = self.task_effective_hours_sum + self.issue_effective_hours_sum

    @api.one
    def _compute_total_timesheets_hours_sum(self):
        timesheet_ids = self.env['account.analytic.line'].search([['account_id', '=', self.analytic_account_id.id], ['is_timesheet', '=', True]])
        self.total_timesheets_hours_sum = sum([timesheet.unit_amount for timesheet in timesheet_ids])

    @api.one
    def _compute_total_difference_estimation_effective_sum(self):
        self.total_difference_estimation_effective_sum = abs(self.task_effective_hours_sum - self.task_planned_hours_sum)

    @api.one
    def _compute_total_timesheets_not_linked_sum(self):
        self.total_timesheets_not_linked_sum = abs(self.total_timesheets_hours_sum - self.total_effective_hours_sum)