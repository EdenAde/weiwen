from openerp import models, fields, api, _
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class project_project_report_methods(models.Model):
    # ---- MODEL IINHERIT
    _inherit = ['project.project']

    # MODEL FIELDS
    issue_per_stage = fields.Char(compute='_compute_issue_per_stage',string="Issue per stage", store=False)
    issue_per_tag = fields.Char(compute='_compute_issue_per_tag',string="Issue per tag", store=False)
    issue_per_priority = fields.Char(compute='_compute_issue_per_priority',string="Issue per priority", store=False)

    task_per_stage = fields.Char(compute='_compute_task_per_stage',string="Task per stage", store=False)
    task_per_tag = fields.Char(compute='_compute_task_per_tag',string="Task per tag", store=False)
    task_per_priority = fields.Char(compute='_compute_task_per_priority',string="Task per priority", store=False)

    # add a field to have issues for project
    issues = fields.One2many('project.issue', 'project_id')

    # ----- ACTION METHODS
    def action_open_print_report_wizard(self, cr, uid, ids, context=None):
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'project_report', 'view_project_report_wizard_print')
        #self.pool.get('project.report.wizard').reset_stats(cr, uid)
        return {
            'name':_("Print Service Report"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'project.report.wizard',
            'res_id': 1,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '',
            'context': {'project_ids': ids,}
        }

    # ----- MODEL METHODS
    def __get_project_report(self):
        cr = self.env.cr
        uid = self.env.user.id
        project_report_obj = self.pool.get('project.report')
        project_report_id = project_report_obj.search(cr, uid, [('id','=',1)])
        if project_report_id:
            return project_report_obj.browse(cr, uid, project_report_id[0])
        raise Exception('Project.report doesn\'t exists')

    def display_issues(self):
        return self.__get_project_report().issues
    def issues_type(self):
        return self.__get_project_report().issues_type
    def issues_stage(self):
        return self.__get_project_report().issues_stage
    def issues_order(self):
        return self.__get_project_report().issues_order

    def display_tasks(self):
        return self.__get_project_report().tasks
    def tasks_type(self):
        return self.__get_project_report().tasks_type
    def tasks_stage(self):
        return self.__get_project_report().tasks_stage
    def tasks_order(self):
        return self.__get_project_report().tasks_order

    def get_comments(self):
        return self.__get_project_report().comments

    def display_project_times(self):
        return self.__get_project_report().project_times
    def display_project_info(self):
        return self.__get_project_report().project_info

    def display_charts(self):
        return self.__get_project_report().show_chart

    def startdate(self):
        startdate = self.__get_project_report().start_date if self.__get_project_report().start_date else datetime.now().strftime('%y-%m-%d')
        return startdate
    def enddate(self):
        end_date = self.__get_project_report().end_date if self.__get_project_report().end_date else datetime.now().strftime('%y-%m-%d')
        return end_date

    def date_application_creation(self):
        return self.__get_project_report().date_application_creation
    def date_application_modified(self):
        return self.__get_project_report().date_application_modified
    def date_application_closed(self):
        return self.__get_project_report().date_application_closed

    def get_user(self):
        return self.env.user.partner_id.name

    def get_filter_issues(self):
        filter = []

        startdate = self.startdate()# if self.startdate() else datetime.now().strftime('%y-%m%d')
        enddate = self.enddate()# if self.enddate() else datetime.now().strftime('%y-%m%d')
        created = self.date_application_creation()
        modified = self.date_application_modified()
        closed = self.date_application_closed()

        filter.append(('project_id', '=', self.id))

        count = 0 + created + modified + closed
        if (count>=2):
            filter.append('|') # if >= 2

        if created:
            filter.append('&')
            filter.append(('create_date', '>=', startdate))
            filter.append(('create_date', '<=', enddate))

        if count == 3:
            filter.append('|') # if = 3

        if modified:
            filter.append('&')
            filter.append(('write_date', '>=', startdate))
            filter.append(('write_date','<=',enddate))
        if closed:
            filter.append('&')
            filter.append(('date_closed', '>=',startdate))
            filter.append(('date_closed','<=',enddate))

        if self.issues_stage() == 'open':
            filter.append(('stage_id.closed', '=', False))
        elif self.issues_stage() == 'closed':
            filter.append(('stage_id.closed', '=', True))
        _logger.debug(filter)

        return filter

    def get_filter_tasks(self):
        filter = []

        startdate = self.startdate()# if self.startdate() else datetime.now().strftime('%y-%m-%d')
        enddate = self.enddate()# if self.enddate() else datetime.now().strftime('%y-%m%-d')
        created = self.date_application_creation()
        modified = self.date_application_modified()
        closed = self.date_application_closed()

        filter.append(('project_id','=',self.id))

        count = 0 + created + modified + closed
        if (count >= 2):
            filter.append('|') # if >= 2

        if created:
            filter.append('&')
            filter.append(('create_date', '>=', startdate))
            filter.append(('create_date', '<=', enddate))

        if count == 3:
            filter.append('|') # if = 3

        if modified:
            filter.append('&')
            filter.append(('write_date', '>=', startdate))
            filter.append(('write_date', '<=', enddate))
        if closed:
            filter.append('&')
            filter.append(('date_end', '>=', startdate))
            filter.append(('date_end', '<=', enddate))
        if self.tasks_stage() == 'open':
            filter.append(('stage_id.closed', '=', False))
        elif self.tasks_stage() == 'closed':
            filter.append(('stage_id.closed', '=', True))
        _logger.debug(filter)

        return filter
        #return ['&', ('create_date', '>=', '2016-02-11'), ('create_date', '<=', '2016-02-11')]

    @api.multi
    def get_issues_for_report(self):
        cr = self.env.cr
        uid = self.env.user.id
        project_issues = self.pool.get('project.issue').search(cr, uid, self.get_filter_issues(), order=self.issues_order())
        project_issues = self.pool.get('project.issue').browse(cr,uid,project_issues)
        _logger.debug('Issues : ')
        _logger.debug(project_issues)
        return project_issues

    @api.multi
    def get_tasks_for_report(self):
        cr = self.env.cr
        uid = self.env.user.id
        project_tasks = self.pool.get('project.task').search(cr, uid, self.get_filter_tasks(), order=self.tasks_order())
        project_tasks = self.pool.get('project.task').browse(cr,uid,project_tasks)
        _logger.debug('Tasks : ')
        _logger.debug(project_tasks)
        return project_tasks

    # copied from sla module
    def _dictionary_to_pie_chart_url(self, dict, colors=False):
        url = "/report/chart/pie?"
        if dict:
            labels = "labels="
            sizes = "sizes="
            keys = dict.keys()
            last = len(keys)-1
            count=0
            for name in keys:
                if count == last:
                    labels += str(name)
                    sizes += str(dict[name])
                else:
                    labels += str(name)+','
                    sizes += str(dict[name])+','
                count+=1
            url = url+labels+"&"+sizes
            if colors:
                color_string = ""
                last = len(colors)-1
                count=0
                for color in colors:
                    if count == last:
                        color_string += color
                    else:
                        color_string += color +','
                url += "&colors="+color_string
        return url

    def _issue_per_stage(self):
        stage_dict = {}
        project_issues = self.get_issues_for_report()
        if project_issues:
            for issue in project_issues:
                if issue.stage_id:
                    user_name = issue.stage_id.name
                    if stage_dict.has_key(user_name):
                        stage_dict[user_name] += 1
                    else:
                        stage_dict[user_name] = 1
        return stage_dict

    # ---- FIELDS COMPUTE METHODS
    @api.one
    def _compute_issue_per_stage(self):
        dict = self._issue_per_stage()
        self.issue_per_stage = self._dictionary_to_pie_chart_url(dict)

    def _issue_per_tag(self):
        stage_dict = {}
        stage_dict['None'] = 0
        project_issues = self.get_issues_for_report()
        if project_issues:
            for issue in project_issues:
                if issue.tag_ids:
                    for tag in issue.tag_ids:
                        tag_name = tag.name
                        if stage_dict.has_key(tag_name):
                            stage_dict[tag_name] += 1
                        else:
                            stage_dict[tag_name] = 1
                else:
                    stage_dict['None'] += 1

        return stage_dict
    @api.one
    def _compute_issue_per_tag(self):
        dict = self._issue_per_tag()
        self.issue_per_tag = self._dictionary_to_pie_chart_url(dict)

    def _issue_per_priority(self):
        stage_dict = {}
        project_issues = self.get_issues_for_report()
        if project_issues:
            for issue in project_issues:
                if issue.priority:
                    user_name = issue.priority
                    if stage_dict.has_key(user_name):
                        stage_dict[user_name] += 1
                    else:
                        stage_dict[user_name] = 1
        return stage_dict

    @api.one
    def _compute_issue_per_priority(self):
        dict = self._issue_per_priority()
        self.issue_per_priority = self._dictionary_to_pie_chart_url(dict)

    # TASKS CHART
    def _task_per_stage(self):
        stage_dict = {}
        project_issues = self.get_tasks_for_report()
        if project_issues:
            for issue in project_issues:
                if issue.stage_id:
                    user_name = issue.stage_id.name
                    if stage_dict.has_key(user_name):
                        stage_dict[user_name] += 1
                    else:
                        stage_dict[user_name] = 1
        return stage_dict

    @api.one
    def _compute_task_per_stage(self):
        dict = self._task_per_stage()
        self.task_per_stage = self._dictionary_to_pie_chart_url(dict)

    def _task_per_tag(self):
        stage_dict = {}
        stage_dict['None'] = 0

        project_tasks = self.get_tasks_for_report()
        if project_tasks:
            for task in project_tasks:
                if task.tag_ids:
                    for tag in task.tag_ids:
                        tag_name = tag.name
                        if stage_dict.has_key(tag_name):
                            stage_dict[tag_name] += 1
                        else:
                            stage_dict[tag_name] = 1
                else:
                    stage_dict['None'] += 1
        return stage_dict

    @api.one
    def _compute_task_per_tag(self):
        dict = self._task_per_tag()
        self.task_per_tag = self._dictionary_to_pie_chart_url(dict)

    def _task_per_priority(self):
        stage_dict = {}
        project_issues = self.get_tasks_for_report()
        if project_issues:
            for issue in project_issues:
                if issue.priority:
                    user_name = issue.priority
                    if stage_dict.has_key(user_name):
                        stage_dict[user_name] += 1
                    else:
                        stage_dict[user_name] = 1
        return stage_dict

    @api.one
    def _compute_task_per_priority(self):
        dict = self._task_per_priority()
        self.task_per_priority = self._dictionary_to_pie_chart_url(dict)
