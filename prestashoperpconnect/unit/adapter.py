from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
from prestashop.prestashop_api import PrestaShopAPI, data2xml, xml2data


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
        schema = self.api.get_schema(self._prestashop_model)
        xml = data2xml(data, schema)
        
        xml = self.api.post(self._prestashop_model, xml)
        data = xml2data(xml)
        return data['id']
        
    def delete(self, ids):
        #pass range of ids to api
        ok = self.api.delete(self._prestashop_model, ids)
        return ok

    def read(self, id, options=None):
        xml = self.api.get(self._prestashop_model, id, options)
        data = xml2data(xml)
        return data

    def search(self, filters):
        return self.api.search(self._prestashop_model, filters)
    
    def write(self, id, data):
        schema = self.api.get_schema(self._prestashop_model)
        xml = data2xml(data, schema)
        ok = self.api.put(self._prestashop_model, id, xml)
        return ok


