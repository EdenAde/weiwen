# -*- coding: utf-8 -*-

{
    'name': "Odoo Service desk",
    'version': '9.0.1.0.0',
    'depends': [
        'project',
        'hr_analytic_timesheet_improvements'
    ],
    'author': "Valentin Thirion, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Project',
    'description': """
Odoo Service Desk

This modules creates an environment for Service Desk People to work, with all their needed forms and views.
This module has been developed by Valentin Thirion @ AbAKUS it-solutions""",
    'data': [
        'views/service_view.xml',
        'views/service_project_issue_view.xml',
        'views/service_project_task_view.xml',
        'views/service_project_timesheet_view.xml',
        'views/service_project_project_view.xml',
    ],
}