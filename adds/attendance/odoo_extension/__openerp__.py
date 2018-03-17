{
    'name': 'ODOO Extension - Vincent',
    'category': 'Hidden',
    'description':
        """
This module provides the core of the OpenERP Extension.
        """,
    'depends': ['website'],
    'auto_install': False,
    'data': ['backend_view.xml', 'frontend_view.xml'],
    'qweb' : ['static/src/xml/backend_template.xml'],
    'bootstrap': False,
}