from openerp.addons.connector.unit.mapper import (
    mapping,
    ExportMapper
)


class PrestaShopExportMapper(ExportMapper):

    def _map_direct(self, record, from_attr, to_attr):
        res = super(PrestaShopExportMapper, self)._map_direct(record,
                                                              from_attr,
                                                              to_attr)
        column = self.model._all_columns[from_attr].column
        if column._type == 'boolean':
            return res and 1 or 0
        return res
