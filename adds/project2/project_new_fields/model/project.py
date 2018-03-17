from openerp import models, fields, api, _

class project_with_info(models.Model):
    _inherit = ['project.project']

    project_description = fields.Text(string="Description")
    attachments_ids = fields.Many2many('ir.attachment', string="Attachments")
