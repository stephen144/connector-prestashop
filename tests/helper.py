import unittest
import random
import string
from ..prestashop.api import PrestaShopAPI


def randomString():
    size = 10
    chars = string.ascii_uppercase
    return string.join(random.choice(chars) for x in range(size))


class PrestaShopTestCase(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls._api = PrestaShopAPI(
            'http://winona/prestashop/api',
            'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L',
        )
        cls._data = {
            'id': 1,
            'name': "Faded Short Sleeves T-shirt",
        }
        cls._xml = """<prestashop>
  <product>
    <id>1</id>
    <name>
      <language>Faded Short Sleeves T-shirt</language>
    </name>
  </product>
</prestashop>"""
