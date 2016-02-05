{
    "name": "Prestashop-Odoo Connector",
    "version": "8.01",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "connector",
    ],
    "author": "SM",
    "description": """
    This module connects Odoo and Prestashop by doing a few exports.
    """,
    "category": "Connector",
    'data': [
        'views/prestashop_model.xml',
        'views/prestashop_menu.xml',
     ],
}
