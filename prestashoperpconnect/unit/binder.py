from openerp.addons.connector.connector import Binder


class PrestashopBinder(Binder):
    """ Generic Binder for Prestshop """

    _external_field = 'prestashop_id'
    _openerp_field = 'odoo_id'
    
