from openerp import models, fields, api, _

class partner_with_projects(models.Model):
    _inherit = ['res.partner']

    tasks_count = fields.Integer(string="Tasks", compute="_compute_tasks")

    @api.multi
    def _compute_tasks(self):
        for partner in self:
            projects = self.env['project.project'].search([['partner_id', '=', partner.id]])
            count = 0
            for project in projects:
                count = count + len(project.task_ids)
            partner.tasks_count = count
            