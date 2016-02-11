from openerp.tests.common import SingleTransactionCase
from openerp.addons.connector.session import ConnectorSession
from ..unit.exporter import export_record
from helper import api, random_string


class TestExporter(SingleTransactionCase):
    
    def setUp(self):
        self.session = ConnectorSession(
            self.env.cr,
            self.env.uid,
            context = self.env.context,
        )
        self.backend = self.env['prestashop.backend'].search([])
        self.backend.ensure_one()

    def test_export_product_create(self):
        product = self.env['product.template'].create({
            'name': random_string(),
            'list_price': 500.00,
        })
        export_record(
            self.session,
            'prestashop.product.template',
            self.backend.id,
            product.id,
        )        
        binding = product.prestashop_bind_ids
        p = api.get('products', binding.prestashop_id)
        name = p.find('./product/name/language').text
        self.assertEqual(product.name, name)

    def test_export_product_edit(self):
        product = self.env['product.template'].create({
            'name': random_string(),
            'list_price': 500.00,
        })
        export_record(
            self.session,
            'prestashop.product.template',
            self.backend.id,
            product.id,
        )
        binding = product.prestashop_bind_ids
        binding.name = "EDIT TEST"
        export_record(
            self.session,
            'prestashop.product.template',
            self.backend.id,
            product.id,
        )

        self.assertEqual(
            binding.prestashop_id,
            product.prestashop_bind_ids.prestashop_id,
        )
        p = api.get('products', binding.prestashop_id)
        name = p.find('./product/name/language').text
        self.assertEqual("EDIT TEST", name)
