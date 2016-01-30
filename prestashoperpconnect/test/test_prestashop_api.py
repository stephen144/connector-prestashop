import unittest
import random
import string
from xml.etree import ElementTree
from requests.exceptions import HTTPError
from prestashop_api import PrestaShopAPI, data2xml


def setNode(xml, node, value):
    tree = ElementTree.fromstring(xml)
    tree[0].find(node).text = str(value)
    return ElementTree.tostring(tree, 'utf-8')

def getNode(xml, node):
    tree = ElementTree.fromstring(xml)
    return tree[0].find(node).text

def randomString():
    chars = string.ascii_uppercase
    size = 10
    return string.join(random.choice(chars) for x in range(size))


class TestSimplePrestaShopAPI(unittest.TestCase):

    def setUp(self):
        self.api = PrestaShopAPI(
            'http://winona/prestashop/api',
            'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L',
        )
        self._prestashop_model = 'customers'

    def test_data2xml(self):
        data = {
            'id': 1,
            'firstname': 'Steee',
        }
        xml = self.dataFunc(data)
        id = getNode(xml, 'id')
        self.assertEqual(id, '1')
        
    @data2xml
    def dataFunc(self, data):
        return data
        
    def test_get(self):
        xml = self.api.get('customers', 1)
        lastName = getNode(xml, 'lastname')
        self.assertEqual(lastName, "DOE")

    def test_post(self):
        xml = self.api.get('customers', 1)
        xml = setNode(xml, 'id', '')
        xml = self.api.post('customers', xml)
        id = getNode(xml, 'id')
        self.assertTrue(id.isdigit())

    def test_put(self):
        xml = self.api.get('customers', 1)
        randomName = randomString()
        xml = setNode(xml, 'firstname', randomName)
        ok = self.api.put('customers', 1, xml)
        self.assertTrue(ok)

        xml = self.api.get('customers', 1)
        firstName = getNode(xml, 'firstname')
        self.assertEqual(firstName, randomName)

    def test_search(self):
        filters = {'filter[reference]': 'demo_1'}
        xml = self.api.search('products', filters)
        tree = ElementTree.fromstring(xml)
        id = tree[0][0].get('id')
        self.assertEqual(id, '1')

        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSimplePrestaShopAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
