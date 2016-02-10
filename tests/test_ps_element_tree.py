from .helper import PrestaShopTestCase, random_string
from xml.etree import ElementTree
from ..prestashop import element_tree as ET


class TestPrestaShopElementTree(PrestaShopTestCase):

    def test_tostring(self):
        e = ElementTree.fromstring(self._xml)
        xml = ET.tostring(e)
        self.assertEqual(self._xml, xml)

    def test_fromstring(self):
        e = ET.fromstring(self._xml)
        name = e.find('name').text
        self.assertEqual(name, "Faded Short Sleeves T-shirt")

    def test_ps_xml_e_set(self):
        self._ps_xml.element = "blah"
        self._ps_xml.xml = "haha"

    def test_ps_xml_data(self):
        data = self._ps_xml.data
        assertEqual(data['name'], "Faded Short Sleeves T-shirt")

        data2 = dict(data)
        random = random_string()
        data2['name'] = random
        xml = ET.PrestaShopXML(self._xml)
        xml.data = data2
        assertEqual(xml.name, random)
        
    def test_ps_xml_get(self):
        self.assertEqual(
            self._ps_xml.name,
            "Faded Short Sleeves T-shirt"
        )

    def test_ps_xml_set(self):
        random = random_string()
        self._ps_xml.name = random
        self.assertTrue(self._ps_xml.name, random)
