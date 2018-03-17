# -*- coding: utf-8 -*-

{
    'name': "Mail Message improvements",
    'version': '9.0.1.0.0',
    'depends': ['mail'],
    'author': "Valentin Thirion, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Social',
    'description': """
This module adds a function on the 'mail.message' object that can be called from a mail template
to get the Project name from an issue or a task.

To have it in the mail, you have to add a called for this method and HTML code to print it.

Example (added in the mail template for message discussion):

% if object.model == 'project.task' or object.model == 'project.issue':
    <h4>Project: ${object.get_project_name()}</h4>
% endif

This module has been developed by Valentin Thirion @ AbAKUS it-solutions""",
    'data': [],
}