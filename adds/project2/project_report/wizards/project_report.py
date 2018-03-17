from openerp import models, fields, api, _
from openerp.osv import osv

class project_report(models.Model):
    # ---- MODEL NAME
    _name = 'project.report'

    # ---- MODEL FIELDS
    project_info = fields.Boolean(string="Show the project info", default=True)
    project_times = fields.Boolean(string="Show the project times", default=True)
    start_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")
    date_application_creation = fields.Boolean(string="Created tasks/issues")
    date_application_modified = fields.Boolean(string="Modified tasks/issues")
    date_application_closed = fields.Boolean(string="Closed tasks/issues")
    show_chart = fields.Boolean(string="Show Chart")
    tasks = fields.Boolean(string="Tasks", default=True)
    tasks_type = fields.Selection([('summary','Summary'),('detailled', 'Detailled')], string='Task presentation', default='summary')
    tasks_order = fields.Selection([('stage_id','Stage'),('name', 'Name')], string="Order by")
    tasks_stage = fields.Selection([("all", "All"), ("open", "Open"), ("closed", "Done & Cancelled")], string="Stages")
    issues = fields.Boolean(string="Issues", default=True)
    issues_type = fields.Selection([('summary','Summary'),('detailled', 'Detailled')], string='Issue presentation', default='summary')
    issues_order = fields.Selection([('stage_id','Stage'),('name', 'Name')], string="Order by")
    issues_stage = fields.Selection([("all", "All"), ("open", "Open"), ("closed", "Done & Cancelled")], string="Stages")
    comments = fields.Text(string="Comments")

class project_report_wizard(osv.osv_memory):
    # ---- MODEL NAME
    _name = 'project.report.wizard'

    # ---- MODEL FIELDS
    project_info = fields.Boolean(string="Show the project info", default=True)
    project_times = fields.Boolean(string="Show the project times", default=True)
    start_date = fields.Date(string="Start date")#, default=_default_start_date)
    end_date = fields.Date(string="End date")#, default=_default_end_date)
    date_application_creation = fields.Boolean(string="Created tasks/issues")
    date_application_modified = fields.Boolean(string="Modified tasks/issues")
    date_application_closed = fields.Boolean(string="Closed tasks/issues")
    show_chart = fields.Boolean(string="Show Chart")
    tasks = fields.Boolean(string="Tasks", default=True)
    tasks_type = fields.Selection([('summary','Summary'),('detailled', 'Detailled')], string='Task presentation', default='summary')
    tasks_order = fields.Selection([('stage_id','Stage'),('name', 'Name')], string="Order by")
    tasks_stage = fields.Selection([("all", "All"), ("open", "Open"), ("closed", "Done & Cancelled")], string="Stages")
    issues = fields.Boolean(string="Issues", default=True)
    issues_type = fields.Selection([('summary','Summary'),('detailled', 'Detailled')], string='Issue presentation', default='summary')
    issues_order = fields.Selection([('stage_id','Stage'),('name', 'Name')], string="Order by")
    issues_stage = fields.Selection([("all", "All"), ("open", "Open"), ("closed", "Done & Cancelled")], string="Stages")
    comments = fields.Text(string="Comments")

    def save(self, cr, uid, ids, context=None):
        project_report_wizard = self.browse(cr, uid, ids[0])
        project_report_obj = self.pool.get('project.report')
        #project.report with id 1 is created in project_report.xml as record
        project_report_obj.write(cr, uid, 1, {
                'project_info':project_report_wizard.project_info,
                'project_times':project_report_wizard.project_times,
                'start_date' : project_report_wizard.start_date,
                'end_date':project_report_wizard.end_date,
                'date_application_creation':project_report_wizard.date_application_creation,
                'date_application_modified':project_report_wizard.date_application_modified,
                'date_application_closed':project_report_wizard.date_application_closed,
                'show_chart':project_report_wizard.show_chart,
                'tasks':project_report_wizard.tasks,
                'tasks_type':project_report_wizard.tasks_type,
                'tasks_order':project_report_wizard.tasks_order,
                'tasks_stage':project_report_wizard.tasks_stage,
                'issues':project_report_wizard.issues,
                'issues_type':project_report_wizard.issues_type,
                'issues_order':project_report_wizard.issues_order,
                'issues_stage':project_report_wizard.issues_stage,
                'comments':project_report_wizard.comments
        })
        return {
                'type': 'ir.actions.act_window_close',
               }

    # ---- ACTION METHODS
    def action_print_report(self, cr, uid, ids, context=None):
        self.save(cr, uid, ids, context)
        project_ids = context.get('project_ids')
        return self.pool['report'].get_action(cr, uid, project_ids, 'project_report.report_project', context=context)
