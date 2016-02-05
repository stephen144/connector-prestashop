import requests
from xml.etree import ElementTree


def data2xml(data, schema):
    tree = ElementTree.fromstring(schema)
    
    for k, v in data.iteritems():
        node = tree[0].find(k)
        
        if node.find('language') is not None:
            node.find('language').text = str(v)
        else:
            node.text = str(v)
    
    xml = ElementTree.tostring(tree, 'utf-8')
    return xml

def xml2data(xml):
    tree = ElementTree.fromstring(xml)
    data = {}
    
    for child in tree[0]:
        data[child.tag] = child.text
    
    return data


class PrestaShopAPI(object):

    def __init__(self, url, key):
        self.url = url
        self.key = key

    def _make_api_url(self, endpoint, id=None):
        url = "{}/{}".format(self.url, endpoint)
        if id:
            url = "{}/{}".format(url, id)
        return url

        # pass range of ids
    def delete(self, endpoint, id):
        url = self._make_api_url(endpoint, id)
        r = requests.delete(url, auth=(self.key, ''))
        return r.ok

    def get(self, endpoint, id, params=None):
        url = self._make_api_url(endpoint, id)
        r = requests.get(url, auth=(self.key, ''), params=params)
        r.raise_for_status()
        return r.text

    def get_schema(self, endpoint):
        params = {'schema': 'blank'}
        return self.get(endpoint, None, params)
    
    def post(self, endpoint, data):
        url = self._make_api_url(endpoint)
        r = requests.post(url, auth=(self.key, ''), data=data)
        r.raise_for_status()
        return r.text
    
    def put(self, endpoint, id, data):
        url = self._make_api_url(endpoint, id)
        r = requests.put(url, auth=(self.key, ''), data=data)
        return r.ok

    def search(self, endpoint, filters):
        return self.get(endpoint, None, filters)
