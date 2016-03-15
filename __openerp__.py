{
    "name": "Prestashop-Odoo Connector",
    "version": "8.0.1.0.0",
    "depends": [
        "sale",
        "connector",
    ],
    "author": "Stephen Medina",
    "company": "Living Stream Ministry",
    "description": """
    This module connects Odoo and Prestashop by doing a few exports.
    """,
    "category": "Connector",
    'data': [
        'views/prestashop_model.xml',
        'views/prestashop_menu.xml',
     ],
}
