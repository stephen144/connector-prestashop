from openerp.addons.connector.unit.synchronizer import Exporter
from openerp.addons.connector.queue.job import job, related_action
from ..connector import get_environment
from ..related_action import unwrap_binding


class PrestaShopExporter(Exporter):
    """ """
    
    def __init__(self, connector_env):
        """ """
        
        super(PrestashopExporter, self).__init__(connector_env)
        self.binding_id = None
        self.prestashop_id = None
        
    def run(self, binding_id):
        """ Run the synchronization """

        # What we are exporting
        self.binding_id = binding_id
        self.prestashop_id = self.binder.to_backend(self.binding_id)

        # Get the values to export
        self.binding = self.model.browse(self.binding_id)
        map_record = self.mapper.map_record(self.binding)

        if self.prestashop_id:
            # The record exists in PS so update it
            data = map_record.values()
            self.backend_adapter.write(self.prestashop_id, data)
        else:
            # The record doesn't exist in PS so create it
            data = map_record.values(for_create=True)
            self.prestashop_id = self.backend_adapter.create(data)

        # Bind the PS record to the Odoo record
        self.binder.bind(self.prestashop_id, self.binding_id)
        
        return "Record exported with PrestaShop ID {}".format(
            self.prestashop_id
        )


@job()
@related_action(action=unwrap_binding)
def export_record(session, model, id):
    """ Export a record to PrestaShop """

    record = session.env[model].browse(id)
    backend_id = record.backend_id.id
    cenv = get_environment(session, model, backend_id)
    
    exporter = cenv.get_connector_unit(PrestaShopExporter)
    return exporter.run(id)
