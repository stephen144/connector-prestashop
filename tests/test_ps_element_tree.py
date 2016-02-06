import unittest
from xml.etree import ElementTree
import ..prestashop.ps_element_tree as ET


class TestPrestaShopElementTree(unittest.TestCase):

    def setUp(self):
        self.xml = """
        <prestashop>
          <product>
            <id>1</id>
            <name>
              <language>Steee</language>
            </name>
          </product>
        </prestashop>
        """

    def test_tostring(self):
        element = ElementTree.fromstring(self.xml)
        xml = ET.tostring(element)
        self.assertEqual(self.xml, xml)

    def test_fromstring(self):
        element = ET.fromstring(self.xml)
        node = element.find('name')
        self.assertEqual(node.text, "Steee")


if __name__ == '__main__':
    unittest.main()
