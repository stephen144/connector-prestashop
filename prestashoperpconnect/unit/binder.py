from openerp.addons.connector.connector import Binder


class PrestaShopBinder(Binder):
    """ Generic Binder for PrestaShop """

    _external_field = 'prestashop_id'
    _openerp_field = 'odoo_id'
    
