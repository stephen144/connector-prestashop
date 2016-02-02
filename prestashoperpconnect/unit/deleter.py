from openerp.addons.connector.unit.synchronizer import Deleter
from openerp.addons.connector.queue.job import job
from ..connector import get_environment


class PrestaShopDeleteSynchronizer(DeleteSynchronizer):
    """ Base deleter for PrestaShop """

    def run(self, external_id):
        """ Run the synchronization, delete the record on PrestaShop

        :param external_id: identifier of the record to delete
        """
        self.backend_adapter.delete(external_id)
        return _('Record %s deleted on PrestaShop') % external_id


@job
def export_delete_record(session, model_name, backend_id, external_id):
    """ Delete a record on PrestaShop """
    env = get_environment(session, model_name, backend_id)
    deleter = env.get_connector_unit(PrestaShopDeleteSynchronizer)
    return deleter.run(external_id)
