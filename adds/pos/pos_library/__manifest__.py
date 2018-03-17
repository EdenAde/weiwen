{
    'name': 'POS library Management',
    'version': '1.0',
    'category': 'Point of Sale',
    'author': 'TL Technology',
    'website': 'http://posodoo.com',
    'price': '0',
    "currency": 'EUR',
    'sequence': 0,
    'depends': ['point_of_sale','library','board','school','res_city','ea_import','label'],
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'view/pos.xml',
        'view/library_action.xml',
        'view/res_config_view.xml',
        'view/library_config.xml',
        'template/pos_main.xml',

        "report/library_report_view.xml",
        "report/school_report_view.xml",
        "report/book_report_view.xml",
        "template/schools_journal.xml",
        "demo/school_demo.xml"
    ],
    'demo': [],
    'test': [],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'installable': True,
    'license': 'LGPL-3',
    'support': 'lehman3087@gmail.com'
}
