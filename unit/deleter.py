from openerp.addons.connector.unit.synchronizer import Deleter
from openerp.addons.connector.queue.job import job
from ..connector.connector import get_environment


class PrestaShopDeleter(Deleter):

    def run(self, prestashop_id):
        self.backend_adapter.delete(prestashop_id)
        return "Record {} was deleted on PrestaShop".format(prestashop_id)


@job
def export_delete_record(session, model, backend_id, prestashop_id):
    cenv = get_environment(session, model, backend_id)
    deleter = cenv.get_connector_unit(PrestaShopDeleteSynchronizer)
    return deleter.run(prestashop_id)
