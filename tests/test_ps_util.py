from .helper import PrestaShopTestCase
from ..prestashop.util import (
    data2xml,
    xml2data,
    getNode,
)


class TestPrestaShopUtil(PrestaShopTestCase):

    def test_data2xml(self):
        schema = self.api.get_schema('products')
        xml = data2xml(self.data, schema)
        self.assertEqual(getNode(xml, 'id'), '1')
        name = "Faded Short Sleeves T-shirt"
        self.assertEqual(getNode(xml, 'name'), name)        

    def test_xml2data(self):
        data = xml2data(self.xml)
        self.assertEqual(data['id'], '1')
        name = "Faded Short Sleeves T-shirt"
        self.assertEqual(data['name'], name)
