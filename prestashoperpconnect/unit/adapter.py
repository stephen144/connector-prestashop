from openerp.addons.connector.unit.backend_adapter import CRUDAdapter


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
        return self.api.get(self._prestashop_model, id, options)

    def create(self, data):
        #xmlTree = data
        return self.api.post(self._prestashop_model, xmlTree)

    def write(self, id, data):
        #get xmlTree
        #xmlTree + data
        return self.api.put(self._prestashop_model, id, xmlTree)

    def delete(self, ids):
        return self.api.delete(self._prestashop_model, ids)
