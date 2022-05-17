# -*- coding: utf-8 -*-
{
    'name': "template_odoo",

    'summary': """
        Base sample template for creating other modules""",

    'description': """
        Base sample template for creating other modules
    """,

    'author': "Kevin A G M",
    'website': "http://www.sistemaagil.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mainmenu.xml',
        'views/person.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'application':True,
    'intallable':True,
}
