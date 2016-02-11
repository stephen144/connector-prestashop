from openerp.addons.connector.unit.synchronizer import Exporter
from openerp.addons.connector.queue.job import job, related_action
from openerp.addons.connector.event import on_record_write
from ..connector.connector import get_environment
#from ..connector.related_action import unwrap_binding


class PrestaShopExporter(Exporter):
    
    def __init__(self, connector_env):
        """ """
        
        super(PrestaShopExporter, self).__init__(connector_env)
        self.binding_id = None
        self.prestashop_id = None
        
    def run(self, odoo_id):
        """ Run the synchronization """

        # Prepare record for export
        unwrap_model = self.binder.unwrap_model()
        record = self.env[unwrap_model].browse(odoo_id)
        binding = record.prestashop_bind_ids
        if not binding:
            binding = self.model.create({
                'backend_id': self.backend_record.id,
                'odoo_id': odoo_id,
            })
        else:
            binding.ensure_one()

        self.binding_id = binding.id
        self.prestashop_id = self.binder.to_backend(binding)
        map_record = self.mapper.map_record(binding)

        if self.prestashop_id:
            # The record exists in PS so update it
            data = map_record.values()
            ok = self.backend_adapter.write(self.prestashop_id, data)
        else:
            # The record doesn't exist in PS so create it
            data = map_record.values(for_create=True)
            self.prestashop_id = self.backend_adapter.create(data)

        # Bind the PS record to the Odoo record
        self.binder.bind(self.prestashop_id, binding)
        
        return "{} {} exported with PrestaShop ID {}".format(
            self._model_name,
            self.binding_id,
            self.prestashop_id,
        )


class PrestaShopBatchExporter(Exporter):

    CHUNK_SIZE = 50
    
    def _record_chunk_generator(self, model, domain):
        offset = 0
        count = self.env[model].search_count(domain)

        while offset < count:
            yield self.env[model].search(
                domain,
                offset = offset,
                limit = self.CHUNK_SIZE,
            )
            offset = offset + self.CHUNK_SIZE
    
    def run(self):

        record_chunks = self._record_chunk_generator(
            self.binder.unwrap_model(),
            [('in_store', '=', True)],
        )
        
        for records in record_chunks:
            for record in records:
                export_record.delay(
                    self.session,
                    self._model_name,
                    self.backend_record.id,
                    record.id,
                    priority = 20,
                )

@job
def export_batch(session, model, backend_id):
    cenv = get_environment(session, model, backend_id)
    exporter = cenv.get_connector_unit(PrestaShopBatchExporter)
    return exporter.run()

            
@job
#@related_action(action=unwrap_binding)
def export_record(session, model, backend_id, odoo_id):
    cenv = get_environment(session, model, backend_id)
    exporter = cenv.get_connector_unit(PrestaShopExporter)
    return exporter.run(odoo_id)


@on_record_write(model_names='prestashop.product.template')
def delay_export_record(session, model, backend_id, odoo_id):
    export_record.delay(session, model, backend_id, priority=20)
