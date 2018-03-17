# -*- coding: utf-8 -*-
{
    'name': "Attendance Record",

    'summary': """Mobile Attendance Record""",

    'description': """
        Attendance Record:
            - Record check in with position
            - Record check out with position
            - Record photo with position
    """,

    'author': "Wangbei",
    'website': "http://www.pay-info.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',

    # any module necessary for this one to work correctly
    'depends': ['base','odoo_extension','report_xls'],

    # always loaded
    'data': [
         'security/attendance_record_security.xml',
         'security/ir.model.access.csv',
         'views.xml',
         'report/attendancetable_xls.xml',
#         'views/partner.xml',
#         'views/session_workflow.xml',
#         'views/session_board.xml',
#         'reports.xml',
    ],
    # only loaded in demonstration mode
#     'demo': [
#         'demo.xml',
#     ],
}