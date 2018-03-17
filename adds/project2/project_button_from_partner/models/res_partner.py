from openerp import models, fields, api, _

class partner_with_projects(models.Model):
    _inherit = ['res.partner']

    open_projects_count = fields.Integer(string="Projects", compute="_compute_open_projects")

    @api.multi
    def _compute_open_projects(self):
        for partner in self:
            projects = self.env['project.project'].search([['partner_id', '=', partner.id]])
            partner.open_projects_count = len(projects)