import unittest
import random
import string
from requests.exceptions import HTTPError
from ..prestashop.prestashop_api import PrestaShopAPI
import ..prestashop.ps_element_tree as ElementTree


def setNode(xml, name, value):
    element = ElementTree.fromstring(xml)
    element.find(name).text = str(value)
    return ElementTree.tostring(element)

def getNode(xml, name):
    element = ElementTree.fromstring(xml)
    return element.find(name).text

def randomString():
    chars = string.ascii_uppercase
    size = 10
    return string.join(random.choice(chars) for x in range(size))


class TestPrestaShopAPI(unittest.TestCase):

    def setUp(self):
        self.api = PrestaShopAPI(
            'http://winona/prestashop/api',
            'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L',
        )
        
    def test_get(self):
        xml = self.api.get('customers', 1)
        self.assertEqual(getNode(xml, 'lastname'), "DOE")

        xml = self.api.get('products', 1)
        self.assertEqual(
            getNode(xml, 'name'),
            "Faded Short Sleeves T-shirt",
        )

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
        self.assertEqual(getNode(xml, 'firstname'), randomName)

    def test_search(self):
        filters = {'filter[reference]': 'demo_1'}
        xml = self.api.search('products', filters)
        element = ElementTree.fromstring(xml)
        id = element[0][0].get('id')
        self.assertEqual(id, '1')

        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPrestaShopAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
