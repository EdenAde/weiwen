from openerp import models, fields, api
from openerp import _
import logging
_logger = logging.getLogger(__name__)

class project_task_assign_itself(models.Model):
    _inherit = ['project.task']

    @api.multi
    def assign_to_me(self):
        for issue in self:
            issue.user_id = self.env.user.id