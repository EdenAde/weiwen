{
    'name': "AbAKUS issue improvements",
    'version': '9.0.1.0.1',
    'depends': ['project_issue'],
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Project',
    'description': 
    """
This modules adds some functionalities to the issues for AbAKUS.

Functionalities:
    - convert issue to task
    - Adds a due date field.
    - Moves the project field on the upper side.
    - Replaces priority stars selection by a normal name selection in the issue form.
    - Replaces priority stars in kanban view by the priority name.
    - Removes "Issues" menuitem from the project module.
    - Adds a fiel 'customer feedback' in Issues
    - Adds "My Issues" and "Unassigned Issues" menuitems in Project.

    - Adds 2 server actions:
        - Project issue email matching. It sets the project from an email issue
        - Project issue email matching + email to SM

odoo 9 Updates:
    - New organisation of fields in issue
    - sale_subscription_id

This module has been developed by Bernard Delhez & Valentin THIRION @ AbAKUS it-solutions.
    """,
    'data': [
        'views/project_issue_view.xml',
        'views/project_task_view.xml',
        'data/ir_actions_server_data.xml',
        'data/project_issue_email_template.xml',
        'data/project_task_stage.xml',
    ],
}
