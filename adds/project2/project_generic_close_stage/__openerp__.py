# -*- coding: utf-8 -*-
{
    'name': "Project Generic Close Stage",

    'summary': """
    """,

    'description': """
        Project Generic Close Stage
        
        Adds a checkbox in stages configuration to define a generic 'close' stage.
        This allows a task/issue to be closed via a button even if no project is linked
        
        This module has been developed by Jason PINDAT, intern @ AbAKUS it-solutions.
    """,

    'author': "Jason PINDAT, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Project',
    'version': '9.0.1.0',

    'depends': ['base', 'project', 'project_issue'],

    'data': [
        'views/project_task_type.xml',
        'views/project_task.xml',
        'views/project_issue.xml',
    ],
}