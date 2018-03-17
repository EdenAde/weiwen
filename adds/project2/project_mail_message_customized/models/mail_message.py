from openerp import models, fields, api

import datetime
import logging
_logger = logging.getLogger(__name__)


class mail_message_improved(models.Model):
    _inherit = 'mail.message'

    @api.model
    def get_project_name(self):
        if self.model == 'project.task' or self.model == 'project.issue':
            related_object = self.env[self.model].search([('id', '=', self.res_id)])
            if (related_object):
                return related_object.project_id.name
        return ""
    