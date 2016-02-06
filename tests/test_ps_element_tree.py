from .helper import PrestaShopTestCase
from xml.etree import ElementTree
from ..prestashop import element_tree as ET


class TestPrestaShopElementTree(PrestaShopTestCase):

    def test_tostring(self):
        element = ElementTree.fromstring(self.xml)
        xml = ET.tostring(element)
        self.assertEqual(self.xml, xml)

    def test_fromstring(self):
        element = ET.fromstring(self.xml)
        node = element.find('name')
        self.assertEqual(node.text, "Faded Short Sleeves T-shirt")
