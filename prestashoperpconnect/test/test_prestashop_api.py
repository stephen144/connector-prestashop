import unittest
from ../unit/prestashop_api import PrestaShopAPI

class TestPrestaShopAPI(unittest.TestCase):

    def setUp(self):
        self.api = PrestaShopAPI(
            'http://winona/prestashop/api',
            'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L',
        )
        self.endpoint = 'customers'
    
    def test_get(self):
        xml = self.api.get(self.endpoint, 1)

if __name__ == '__main__':
    unittest.main()
