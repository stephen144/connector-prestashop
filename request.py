from xml.etree import ElementTree
from xml.dom import minidom
import requests


def pp(elem):
    return ElementTree.tostring(elem, 'utf-8')

def pprint(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


class PrestaShopAPI(object):

    def __init__(self, url, key):
        self.url = url
        self.key = key

    def make_api_url(self, endpoint, id=None):
        url = "{}/{}".format(self.url, endpoint)
        if id:
            url = "{}/{}".format(url, id)
        return url

    def get_xml_schema(self, endpoint):
        params = {'schema': 'blank'}
        return self.get(endpoint, None, params)
    
    def search(self, endpoint, params):
        return self.get(endpoint, None, params)
    
    def get(self, endpoint, id, params=None):
        url = self.make_api_url(endpoint, id)
        
        r = requests.get(url, auth=(self.key, ''), params=params)
        r.raise_for_status()
        
        xmlTree = ElementTree.fromstring(r.text)
        return xmlTree

    def put(self, endpoint, id, xmlTree):
        url = self.make_api_url(endpoint, id)
        xml = ElementTree.tostring(xmlTree, 'utf-8')
        
        r = requests.put(url, auth=(self.key, ''), data=xml)
        r.raise_for_status()
        
        return r.status_code == requests.codes.ok
    
    def post(self, endpoint, xmlTree):
        url = self.make_api_url(endpoint)
        xml = ElementTree.tostring(xmlTree, 'utf-8')
        
        r = requests.post(url, auth=(self.key, ''), data=xml)
        r.raise_for_status()
        
        xmlTree = ElementTree.fromstring(r.text)
        return xmlTree


if __name__ == '__main__':
    url = 'http://winona/prestashop/api'
    key = 'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L'
    api = PrestaShopAPI(url, key)

    #api.get('customers', 1)




