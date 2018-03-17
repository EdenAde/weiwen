# -*- coding: utf-8 -*-
{
    'name': "Merge Tasks and Issues",

    'summary': """
        The merge_tasks_wizard / merge_issues_wizard module merges multiple tasks/issues into one,
                """,
    'description': """
        Merging multiple tasks into one is now possible with this module.
        Go to Project --> Tasks (list view) and select multiple tasks, in the action button
        there will be Merge Tasks option. The wizard will open and place your settings there.

        Adapted by Valentin Thirion @ AbAKUS:
        Merging multiple issues into one is now possible with this module.
        Go to Project --> Issues (list view) and select multiple issues, in the action button
        there will be Merge Issues option. The wizard will open and place your settings there.

    """,

    'author': "Cona Cons (RISTE KABRANOV) & Valentin THIRION @ AbAKUS it-solutions",
    'website': "http://simplify-erp.com",
    'category': 'Project, Tasks',
    'version': '9.0.1.0.0',
    'depends': [
        'base',
        'project',
        'project_timesheet'
    ],
    'data': [
        'views/project_task_view.xml',
        'views/project_issue_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
