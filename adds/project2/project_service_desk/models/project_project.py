from openerp import models, fields, api, _

class project_service_desk(models.Model):
    _inherit = ['project.project']

    project_type = fields.Selection([('support', 'Support'), ('installation', 'Installation'), ('internal', 'Internal'), ('development', 'Development'), ('other', 'Other')], 'Type of Project')

    defaults = {
        'project_type ': lambda self, cr, uid, ctx=None: self._get_default_project_type(cr, uid, context=ctx)
    }

    def _get_default_project_type(self, cr, uid, context=None):
        if context is None:
            context = {}
        if 'default_project_type' in context:
            if context['default_project_type']:
                return context['default_project_type']    
        return False
