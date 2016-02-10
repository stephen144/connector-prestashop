import requests
from element_tree import PrestaShopXML
        

def make_api_url(url, endpoint, id=None):
    api_url = "{}/{}".format(url, endpoint)
    if id:
        api_url = "{}/{}".format(api_url, id)
    return api_url


class PrestaShopAPI(object):

    def __init__(self, url, key):
        self.url = url
        self.auth = (key, '')

    # pass range of ids
    def delete(self, endpoint, id):
        url = make_api_url(self.url, endpoint, id)
        r = requests.delete(url, auth=self.auth)
        return r.ok

    def get(self, endpoint, id, params=None):
        url = make_api_url(self.url, endpoint, id)
        r = requests.get(url, auth=self.auth, params=params)
        r.raise_for_status()
        return PrestaShopXML(r.text)

    def get_schema(self, endpoint):
        params = {'schema': 'blank'}
        return self.get(endpoint, None, params)
    
    def post(self, endpoint, data):
        url = make_api_url(self.url, endpoint)
        r = requests.post(url, auth=self.auth, data=str(data))
        r.raise_for_status()
        return PrestaShopXML(r.text)
    
    def put(self, endpoint, id, data):
        url = make_api_url(self.url, endpoint, id)
        r = requests.put(url, auth=self.auth, data=str(data))
        return r.ok

    def search(self, endpoint, filters):
        return self.get(endpoint, None, filters)
