from openerp.tests.common import SingleTransactionCase
from openerp.addons.connector.session import ConnectorSession
from helper import (
    PrestaShopTransactionCase,
    api,
)
from ..unit.exporter import export_record


class PrestaShopTransactionCase(SingleTransactionCase):
    
    def setUp(self):
        self.session = ConnectorSession(
            self.env.cr,
            self.env.uid,
            context = self.env.context,
        )
        self.backend = self.env['prestashop.backend'].search([])
        self.backend.ensure_one()
        self.product = self.env['product.template'].create({
            'name': random_string(),
            'sale_price': 500.00,
        })


class TestExporter(PrestaShopTransactionCase):

    def test_export_product(self):
        export_record(
            self.session,
            'prestashop.product.template',
            self.backend.id,
            self.product.id,
        )
        binding = self.product.prestashop_bind_ids
        self.assertTrue(binding)
        prestashop_id = binding.prestashop_id
        self.assertTrue(prestashop_id.isdigit())
        
        xml = api.get('products', prestashop_id)
        name = getNode(xml, 'name')
        assertTre(product.name, name)
