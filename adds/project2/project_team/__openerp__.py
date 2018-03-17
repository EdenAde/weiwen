# -*- coding: utf-8 -*-

{
    'name':'Project Team',
    'author':'Valentin Thirion @ AbAKUS it-solutions',
    'summary':'Adds Project Team Members.',
    'category': 'Project Management.',
    'website':'http://www.abakusitsolutions.eu',
    'version':'9.0.1.0.0',
    'depends': [
        'project'
    ],
    'data':[
        'views/project_team_view.xml',
        'views/project_issue_view.xml',
        'views/project_task_view.xml',
        'views/project_project_view.xml',

        'security/ir.model.access.csv',
    ],
    'installable':True,
}