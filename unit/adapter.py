from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
from ..prestashop.api import PrestaShopAPI
from ..prestashop.util import populate, todict


class PrestaShopAdapter(CRUDAdapter):
    _model_name = None
    _prestashop_model = None
    
    def __init__(self, environment):
        super(PrestaShopAdapter, self).__init__(environment)
        self.api = PrestaShopAPI(
            self.backend_record.location,
            self.backend_record.key
        )

    def create(self, data):
        e = self.api.get_schema(self._prestashop_model)
        populate(e, data)
        e = self.api.post(self._prestashop_model, e)
        return e.find('./*[1]/id').text
        
    def delete(self, ids):
        #pass range of ids to api
        ok = self.api.delete(self._prestashop_model, ids)
        return ok

    def read(self, id, options=None):
        e = self.api.get(self._prestashop_model, id, options)
        return todict(e)

    def search(self, filters):
        return self.api.search(self._prestashop_model, filters)
    
    def write(self, id, data):
        e = self.api.get(self._prestashop_model, id)
        populate(e, data)
        ok = self.api.put(self._prestashop_model, id, e)
        return ok


