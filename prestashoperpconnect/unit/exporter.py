from openerp.addons.connector.unit.synchronizer import Exporter
from openerp.addons.connector.queue.job import job, related_action
from ..connector import get_environment


class PrestashopExporter(Exporter):
    """
    Exporters for Prestashop.

    In addition to its export job, an exporter has to:

    * check in Prestashop if the record has been updated more recently than the
    last sync date and if yes, delay an import
    * call the ``bind`` method of the binder to update the last sync date

    """


    def __init__(self, connector_env):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.Environment`
        """
        super(PrestashopExporter, self).__init__(connector_env)
        self.binding_id = None
        self.prestashop_id = None
        
    def _get_openerp_data(self):
        """ Return the raw OpenERP data for ``self.binding_id`` """
        return self.model.browse(self.binding_id)

    def run(self, binding_id, *args, **kwargs):
        """ Run the synchronization

        :param binding_id: identifier of the binding record to export
        """
        self.binding_id = binding_id
        self.binding_record = self._get_openerp_data()

        self.prestashop_id = self.binder.to_backend(self.binding_id)
        result = self._run(*args, **kwargs)

        self.binder.bind(self.prestashop_id, self.binding_id)
        # Commit so we keep the external ID when there are several
        # exports (due to dependencies) and one of them fails.
        # The commit will also release the lock acquired on the binding
        # record
        self.session.commit()

        self._after_export()
        return result

    def _run(self):
        """ Flow of the synchronization, implemented in inherited classes"""
        raise NotImplementedError

    def _after_export(self):
        """ Can do several actions after exporting a record on magento """
        pass

    
class PrestashopExporter(PrestashopBaseExporter):
    """ A common flow for the exports to Prestashop """

    def __init__(self, environment):
        """
        :param environment: current environment (backend, session, ...)
        :type environment: :py:class:`connector.connector.Environment`
        """
        super(PrestashopExporter, self).__init__(environment)
        self.erp_record = None

    def _has_to_skip(self):
        """ Return True if the export can be skipped """
        return False

    def _export_dependencies(self):
        """ Export the dependencies for the record"""
        return

    def _map_data(self, fields=None):
        """ Convert the external record to OpenERP """
        self.mapper.convert(self.erp_record, fields=fields)

    def _validate_data(self, data):
        """ Check if the values to import are correct

        Pro-actively check before the ``Model.create`` or
        ``Model.update`` if some fields are missing

        Raise `InvalidDataError`
        """
        return

    def _create(self, data):
        """ Create the Prestashop record """
        return self.backend_adapter.create(data)

    def _update(self, data):
        """ Update an Prestashop record """
        assert self.prestashop_id
        self.backend_adapter.write(self.prestashop_id, data)

    def _run(self, fields=None):
        """ Flow of the synchronization, implemented in inherited classes"""
        assert self.binding_id
        assert self.erp_record

        if not self.prestashop_id:
            fields = None  # should be created with all the fields

        if self._has_to_skip():
            return

        # export the missing linked resources
        self._export_dependencies()

        self._map_data(fields=fields)

        if self.prestashop_id:
            record = self.mapper.data
            if not record:
                return _('Nothing to export.')
            # special check on data before export
            self._validate_data(record)
            self._update(record)
        else:
            record = self.mapper.data_for_create
            if not record:
                return _('Nothing to export.')
            # special check on data before export
            self._validate_data(record)
            self.prestashop_id = self._create(record)
        message = _('Record exported with ID %s on Prestashop.')
        return message % self.prestashop_id

@job(default_channel='root.prestashop')
@related_action(action=unwrap_binding)
def export_record(session, model_name, binding_id):
    """ Export a record on Prestashop """

    record = session.env[model_name].browse(binding_id)
    backend_id = record.backend_id.id
    cenv = get_environment(session, model_name, backend_id)
    exporter = cenv.get_connector_unit(PrestashopExporter)
    return exporter.run(binding_id)
