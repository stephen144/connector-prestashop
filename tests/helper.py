import random
import string
from unittest import TestCase
from ..prestashop.api import PrestaShopAPI
#from ..prestashop.element_tree import fromstring


api = PrestaShopAPI(
    'http://winona/prestashop/api',
    'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L',
)


def random_string():
    size = 10
    chars = string.ascii_uppercase
    return string.join(random.choice(chars) for x in range(size))


class PrestaShopTestCase(TestCase):

    @classmethod
    def setUp(cls):
        cls.data = {
            'id': 1,
            'name': "Faded Short Sleeves T-shirt",
        }
        cls.xml = """<prestashop>
  <product>
    <id>1</id>
    <name>
      <language>Faded Short Sleeves T-shirt</language>
    </name>
  </product>
</prestashop>"""
        #cls.e = fromstring(cls.xml)
