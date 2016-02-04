import openerp.addons.connector.backend as backend

prestashop = backend.Backend('prestashop')
prestashop1614 = backend.Backend(parent=prestashop, version='1.6.1.4')
