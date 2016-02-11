from .helper import PrestaShopTestCase, api
from ..prestashop.util import populate, todict


class TestPrestaShopUtil(PrestaShopTestCase):

    def test_populate(self):
        p = api.get_schema('products')
        populate(p, self.data)
        name = p.find('./product/name/language').text
        self.assertEqual(name, self.data['name'])

    def test_todict(self):
        p = api.get('products', 1)
        data = todict(p)
        self.assertEqual(data['name'], self.data['name'])
        self.assertEqual(data['id'], str(self.data['id']))
