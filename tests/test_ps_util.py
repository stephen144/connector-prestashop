import unittest
from ..prestashop.util import data2xml, xml2data
from ..prestashop.prestashop_api import PrestaShopAPI
from test_prestashop_api import getNode


class TestPrestaShopUtil(unittest.TestCase):

    def setUp(self):
        self.api = PrestaShopAPI(
            'http://winona/prestashop/api',
            'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L',
        )
        self.data = {
            'id': 1,
            'firstname': 'Steee',
        }
        self.xml = """
        <prestashop>
          <customer>
            <id>1</id>
            <firstname>Steee</firstname>
          </customer>
        </prestashop>
        """

    def test_data2xml(self):
        schema = self.api.get_schema('customers')
        xml = data2xml(self.data, schema)
        self.assertEqual(getNode(xml, 'id'), '1')
        self.assertEqual(getNode(xml, 'firstname'), "Steee")        

    def test_xml2data(self):
        data = xml2data(self.xml)
        self.assertEqual(data['id'], '1')
        self.assertEqual(data['firstname'], "Steee")
