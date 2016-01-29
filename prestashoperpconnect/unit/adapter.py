from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
from prestashop_api import (PrestaShopAPI, data2xml)
    

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
        
    def search(self, filters):
        return self.api.search(self._prestashop_model, filters)

    def read(self, id, options=None):
        xml = self.api.get(self._prestashop_model, id, options)
        return xml

    @data2xml
    def create(self, data):
        xml = self.api.post(self._prestashop_model, data)
        #return id??
        return xml

    @data2xml
    def write(self, id, data):
        ok = self.api.put(self._prestashop_model, id, data)
        return ok

    def delete(self, ids):
        #pass range of ids to api
        ok = self.api.delete(self._prestashop_model, ids)
        return ok
