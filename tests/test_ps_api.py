from .helper import PrestaShopTestCase, random_string, api
from ..prestashop.api import PrestaShopAPI


class TestPrestaShopAPI(PrestaShopTestCase):

    def test_get(self):
        c = api.get('customers', 1)
        self.assertEqual(c.lastname, "DOE")

        p = api.get('products', 1)
        self.assertEqual(
            p.name,
            "Faded Short Sleeves T-shirt",
        )

    def test_post(self):
        c = api.get('customers', 1)
        c.id = ''
        c = api.post('customers', c)
        self.assertTrue(c.id.isdigit())

    def test_put(self):
        c = api.get('customers', 1)
        randomName = random_string()
        c.firstname = randomName
        
        ok = api.put('customers', 1, c)
        self.assertTrue(ok)

        c = api.get('customers', 1)
        self.assertEqual(c.firstname, randomName)

    def test_search(self):
        filters = {'filter[reference]': 'demo_1'}
        p = api.search('products', filters)
        firstChild = p.children[0]
        self.assertEqual(firstChild.get('id'), '1')
