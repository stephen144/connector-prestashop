from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
from prestapyt import PrestaShopWebServiceDict


class PrestaShopLocation(object):

    def __init__(self, location, webservice_key):
        self.location = location
        self.webservice_key = webservice_key
        self.api_url = '%s/api' % location


class PrestaShopCRUDAdapter(CRUDAdapter):
    """ External Records Adapter for PrestaShop """

    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.Environment`
        """
        
        super(PrestaShopCRUDAdapter, self).__init__(environment)
        self.prestashop = PrestaShopLocation(
            self.backend_record.location,
            self.backend_record.webservice_key
        )


class PrestaShopAdapter(PrestaShopCRUDAdapter):
    """
    """
    
    _model_name = None
    _prestashop_model = None
    _export_node_name = None

    def connect(self):
        #UX476CTV4XM3VMTUX7F235YGC4YG5LWW
        return PrestaShopWebServiceDict(
            self.prestashop.api_url,
            self.prestashop.webservice_key
        )

    def search(self, filters=None):
        """ Search records according to some criterias
        and returns a list of ids

        :rtype: list
        """
        api = self.connect()
        return api.search(self._prestashop_model, filters)

    def read(self, id, options=None):
        """ Returns the information of a record

        :rtype: dict
        """

        api = self.connect()
        res = api.get(self._prestashop_model, id, options=options)
        first_key = res.keys()[0]
        return res[first_key]

    def create(self, attributes=None):
        """ Create a record on the external system """
        
        api = self.connect()
        return api.add(self._prestashop_model, {
            self._export_node_name: attributes
        })

    def write(self, id, attributes=None):
        """ Update records on the external system """
        
        api = self.connect()
        attributes['id'] = id
        return api.edit(self._prestashop_model, {
            self._export_node_name: attributes
        })

    def delete(self, ids):
        """ Delete records on the external system """
        
        api = self.connect()
        return api.delete(self._prestashop_model, ids)
