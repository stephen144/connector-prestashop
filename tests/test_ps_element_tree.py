from .helper import PrestaShopTestCase
from xml.etree import ElementTree
from ..prestashop import element_tree as ET


class TestPrestaShopElementTree(PrestaShopTestCase):

    def test_tostring(self):
        e = ElementTree.fromstring(self._xml)
        xml = ET.tostring(e)
        self.assertEqual(self._xml, xml)

    def test_fromstring(self):
        import pdb; pdb.set_trace()
        e = ET.fromstring(self._xml)
        node = e.find('name')
        name = node.text
        self.assertEqual(name, "Faded Short Sleeves T-shirt")
