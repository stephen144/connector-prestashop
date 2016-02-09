from .helper import PrestaShopTestCase, randomString
from ..prestashop import element_tree as ElementTree
from ..prestashop.api import PrestaShopAPI
from ..prestashop.util import getNode, setNode

import unittest
@unittest.skip("showing class skipping")
class TestPrestaShopAPI(PrestaShopTestCase):

    def test_get(self):
        xml = self._api.get('customers', 1)
        self.assertEqual(getNode(xml, 'lastname'), "DOE")

        xml = self._api.get('products', 1)
        self.assertEqual(
            getNode(xml, 'name'),
            "Faded Short Sleeves T-shirt",
        )

    def test_post(self):
        xml = self._api.get('customers', 1)
        xml = setNode(xml, 'id', '')
        xml = self._api.post('customers', xml)
        id = getNode(xml, 'id')
        self.assertTrue(id.isdigit())

    def test_put(self):
        xml = self._api.get('customers', 1)
        randomName = randomString()
        xml = setNode(xml, 'firstname', randomName)
        
        ok = self._api.put('customers', 1, xml)
        self.assertTrue(ok)

        xml = self._api.get('customers', 1)
        self.assertEqual(getNode(xml, 'firstname'), randomName)

    def test_search(self):
        filters = {'filter[reference]': 'demo_1'}
        xml = self._api.search('products', filters)
        e = ElementTree.fromstring(xml)
        id = e[0].get('id')
        self.assertEqual(id, '1')
