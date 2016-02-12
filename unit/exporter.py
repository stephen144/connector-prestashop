from openerp.addons.connector.unit.synchronizer import Exporter
from openerp.addons.connector.queue.job import job, related_action
from openerp.addons.connector.event import on_record_write
from ..connector.connector import get_environment
#from ..connector.related_action import unwrap_binding


class PrestaShopExporter(Exporter):

    """
    def __init__(self, connector_env):
        super(PrestaShopExporter, self).__init__(connector_env)
        self.binding_id = None
        self.prestashop_id = None
    """
    
    # assuming I don't have to assign record.prestashop_bind_ids
    def _get_or_create_binding(self, odoo_id):
        model = self.binder.unwrap_model(self._model_name)
        record = self.env[model].browse(odoo_id)
        binding = record.prestashop_bind_ids
        if len(binding) == 0:
            binding = self.model.create({
                'backend_id': self.backend_record.id,
                'odoo_id': record.id,
            })
        binding.ensure_one()
        return binding
    
    def run(self, odoo_id):
        binding = self._get_or_create_binding(odoo_id)
        #self.binding_id = binding.id
        #self.prestashop_id = self.binder.to_backend(binding)
        prestashop_id = self.binder.to_backend(binding)
        map_record = self.mapper.map_record(binding)

        if prestashop_id is not None:
            # The record exists in PS so update it
            data = map_record.values()
            ok = self.backend_adapter.write(prestashop_id, data)
            #check ok
        else:
            # Record doesn't appear to exist in PS; check for sure
            filters = {'reference': binding.default_code}
            prestashop_id = self.backend_adapter.search(filters)
            
            if prestashop_id is None:
                data = map_record.values(for_create=True)
                prestashop_id = self.backend_adapter.create(data)
                # check?

        # Bind the PS record to the Odoo record
        self.binder.bind(prestashop_id, binding)
        
        return "{} {} exported with PrestaShop ID {}".format(
            self._model_name,
            self.binding.id,
            prestashop_id,
        )


class PrestaShopBatchExporter(Exporter):

    def __init__(self):
        super(PrestaShopBatchExporter, self).__init__()
        self._chunk_size = 50
        
    @property
    def chunk_size(self):
        return self._chunk_size

    def _record_chunk_generator(self, model, domain):
        offset = 0
        count = self.env[model].search_count(domain)

        while offset < count:
            yield self.env[model].search(
                domain,
                offset = offset,
                limit = self.chunk_size,
            )
            offset = offset + self.chunk_size
            
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

# TODO: write a test for this
@on_record_write(model_names='prestashop.product.template')
def delay_export_record(session, model, backend_id, odoo_id):
    export_record.delay(session, model, backend_id, priority=20)
