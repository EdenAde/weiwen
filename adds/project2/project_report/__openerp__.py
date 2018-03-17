{
    'name': "Project Report",
    'version': '9.0.1.0.4',
    'depends': ['report', 'project'],
    'author': "Quentin Tawry, AbAKUS it-solutions PGmbH",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'project',
    'description':
    """
This modules adds a report and wizard on projects in order to print a beautiful report containing all information an data for this project.

It is possible to see Issues, Tasks (summarized or fully detailed) as well as charts for some info.

This module has been developed by Quentin TAWRY @ AbAKUS it-solutions
    """,
    'data': [
        'data/project_report_data.xml',
        'views/project_project_view.xml',
        'reports/project_report.xml',
        'wizards/project_report_view.xml',
        'security/ir.model.access.csv',
    ],
}
