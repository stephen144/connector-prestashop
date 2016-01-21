from openerp.addons.connector.unit.backend_adapter import CRUDAdapter
from prestapyt import PrestaShopWebService, PrestShopWebServiceError


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
    _api_node_name = None

    def connect(self):
        #UX476CTV4XM3VMTUX7F235YGC4YG5LWW
        return PrestaShopWebService(
            self.prestashop.api_url,
            self.prestashop.webservice_key
        )

    def search(self, options=None):
        """ Search records according to some criterias
        and returns a list of ids

        options is a dict

        :rtype: elem
        """
        api = self.connect()
        return api.search(self._prestashop_model, options)

    def read(self, id, options=None):
        """
        Returns the information of a record

        :rtype: Element
        """

        api = self.connect()
        data = api.get(self._prestashop_model, id, options)
        return data

    def create(self, data=None):
        """
        Create a record on the external system

        data is a dict from mapper
        """
        
        api = self.connect()
        #wrap data dict in elem
        return api.add(self._prestashop_model, data)

    def write(self, id, data=None):
        """ Update records on the external system

        data is dict from mapper
        """
        
        api = self.connect()
        #wrap data dict in elem
        return api.edit(
            self._prestashop_model,
            id,
            data,
        )

    def delete(self, ids):
        """ Delete records on the external system """
        
        api = self.connect()
        return api.delete(self._prestashop_model, ids)
