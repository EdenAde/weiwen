# -*- coding: utf-8 -*-

{
    'name': "Close Tasks and Issues from list",
    'version': '9.0.1.0.1',
    'depends': [
        'project',
        'project_issue'
    ],
    'author': "Valentin Thirion, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Project',
    'description': """
Close tasks and issues from batch

Now you can select one or more tasks and issues from tree views and click "Action/Close Issue(s)/Tasks(s)" to set the "closed" stage related to the project of the select elements.

This module has been developed by Valentin Thirion @ AbAKUS it-solutions""",
    'data': [
        'wizard/project_close_task_issue_from_list_wizard.xml',
    ],
}