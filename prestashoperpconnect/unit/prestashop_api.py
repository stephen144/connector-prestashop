from xml.etree import ElementTree
import requests


def data2xml(func):
    def wrapper(self, data):
        xml = self.api.get_schema(self._prestashop_model)
        xmlTree = ElementTree.fromstring(xml)
        dataNode = xmlTree[0]
        
        for k, v in data.iteritems():
            dataNode.find(k).text = v

        xmlTree[0] = dataNode
        xml = ElementTree.tostring(xmlTree, 'utf-8')
        return func(self, xml)
    
    return wrapper


class PrestaShopAPI(object):

    def __init__(self, url, key):
        self.url = url
        self.key = key

    def _make_api_url(self, endpoint, id=None):
        url = "{}/{}".format(self.url, endpoint)
        if id:
            url = "{}/{}".format(url, id)
        return url

    def get_schema(self, endpoint):
        params = {'schema': 'blank'}
        return self.get(endpoint, None, params)
    
    def search(self, endpoint, filters):
        return self.get(endpoint, None, filters)
    
    def get(self, endpoint, id, params=None):
        url = self._make_api_url(endpoint, id)
        r = requests.get(url, auth=(self.key, ''), params=params)
        r.raise_for_status()
        return r.text

    def put(self, endpoint, id, data):
        url = self._make_api_url(endpoint, id)
        r = requests.put(url, auth=(self.key, ''), data=data)
        return r.ok
    
    def post(self, endpoint, data):
        url = self._make_api_url(endpoint)
        r = requests.post(url, auth=(self.key, ''), data=data)
        r.raise_for_status()
        return r.text

    # pass range of ids
    def delete(self, endpoint, id):
        url = self._make_api_url(endpoint, id)
        r = requests.delete(url, auth=(self.key, ''))
        return r.ok


if __name__ == '__main__':
    url = 'http://winona/prestashop/api'
    key = 'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L'
    api = PrestaShopAPI(url, key)
    data = {
        'id': '5',
        'firstname': 'Steee',
    }
    
    class Test():
        def __init__(self):
            self.api = api
            self._prestashop_model = 'customers'
                
        @data2xml
        def test(self, data):
            return data

    mytest = Test()
    print(mytest.test(data))
