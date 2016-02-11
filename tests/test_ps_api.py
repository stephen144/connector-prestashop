from .helper import PrestaShopTestCase, random_string, api


class TestPrestaShopAPI(PrestaShopTestCase):

    def test_get(self):
        c = api.get('customers', 1)
        lastname = c.find('./customer/lastname').text
        self.assertEqual(lastname, "DOE")

        p = api.get('products', 1)
        name = p.find('./product/name/language').text
        self.assertEqual(
            name,
            "Faded Short Sleeves T-shirt",
        )

    def test_post(self):
        c = api.get('customers', 1)
        c.find('./customer/id').text = ''
        
        c = api.post('customers', c)
        id = c.find('./customer/id').text
        self.assertTrue(id.isdigit())

    def test_put(self):
        c = api.get('customers', 1)
        randomName = random_string()
        c.find('./customer/firstname').text = randomName
        
        ok = api.put('customers', 1, c)
        self.assertTrue(ok)

        c = api.get('customers', 1)
        firstname = c.find('./customer/firstname').text
        self.assertEqual(firstname, randomName)

    def test_search(self):
        filters = {'filter[reference]': 'demo_1'}
        p = api.search('products', filters)
        id = p.find('./products/*').get('id')
        self.assertEqual(id, '1')
