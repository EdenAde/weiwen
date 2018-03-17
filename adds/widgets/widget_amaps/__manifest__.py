# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Widget gaode Maps',
    'sequence': 10,
    'description': """

    """,
    'author': 'lehman',
    'category': 'OpenERP  widgets',
    'depends': [
    ],
    'init_xml': [
    ],
    'data': [
        'views/widget_amaps.xml',
    ],
    'qweb': [
        'static/src/xml/resource.xml'
    ],
    'installable': True,
    'application': True,
    'bootstrap': True,
}