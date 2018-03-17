from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class task_from_issue(models.Model):
    _inherit = ['project.task']

    origin_issue = fields.Many2one('project.issue', string="Origin Issue")
    origin_issue_state = fields.Char(string="Origin Issue State", compute="_compute_origin_issue_state")

    @api.onchange('origin_issue')
    def _compute_origin_issue_state(self):
        for issue in self:
            if issue.origin_issue.id != False and issue.origin_issue.name != '':
                issue.origin_issue_state = issue.origin_issue.stage_id.name

