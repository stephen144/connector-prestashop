import unittest
import random
from openerp.addons.connector.session import ConnectorSession
from test_prestashop_api import (
    randomString,
    getNode,
)
from ..unit.exporter import (
    PrestaShopExporter,
    export_record,
)
from ..prestashop.prestashop_api import PrestaShopAPI

class TestExporter(unittest.TestCase):

    def setUp(self):
        self.session = ConnectorSession(
            self.env.cr,
            self.env.uid,
            context = self.env.context,
        )
        self.product = self.env['product.template'].create({
            'name': randomString(),
            'sale_price': 500.00,
        })
        self.backend = self.env['prestashop.backend'].search([])
        self.backend.ensure_one()
        self.api = PrestaShopAPI(
            'http://winona/prestashop/api',
            'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L',
        )
        

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
        xml = self.api.get('products', prestashop_id)
        name = getNode(xml, 'name')

        
