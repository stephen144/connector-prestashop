from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
from prestashop_api import PrestaShopAPI
from xml.etree import ElementTree


def dict2xmltest(func):
    def wrapper(self, data):
        xml = self.api.get_schema(self._prestashop_model)
        tree = ElementTree.fromstring(xml)
        dataNode = tree[0]
        
        for k, v in data.iteritems():
            dataNode.find(k).text = str(v)

        tree[0] = dataNode
        xml = ElementTree.tostring(tree, 'utf-8')
        return func(self, xml)
    
    return wrapper

def dict2xml(data, model):
    xml = self.api.get_schema(model)
    tree = ElementTree.fromstring(xml)
    
    for k, v in data.iteritems():
        tree[0].find(k).text = str(v)
    
    xml = ElementTree.tostring(tree, 'utf-8')
    return xml           

def xml2dict(xml):
    tree = ElementTree.fromstring(xml)
    dataNode = tree[0]
    data = {}
    
    for child in dataNode:
        data[child.tag] = child.text
    
    return data
    


class PrestaShopCRUDAdapter(CRUDAdapter):
    """
    External Records Adapter for PrestaShop
    """

    _model_name = None
    _prestashop_model = None
    
    def __init__(self, environment):
        super(PrestaShopCRUDAdapter, self).__init__(environment)
        self.api = PrestaShopAPI(
            self.backend_record.location,
            self.backend_record.webservice_key
        )

    def create(self, data):
        data = dict2xml(data)
        result = self.api.post(self._prestashop_model, data)
        
        #return id??
        return xml
        
    def delete(self, ids):
        #pass range of ids to api
        ok = self.api.delete(self._prestashop_model, ids)
        return ok

    def read(self, id, options=None):
        xml = self.api.get(self._prestashop_model, id, options)
        data = xml2dict(xml)
        return data

    def search(self, filters):
        return self.api.search(self._prestashop_model, filters)
    
    def write(self, id, data):
        data = dict2xml(data)
        ok = self.api.put(self._prestashop_model, id, data)
        return ok


