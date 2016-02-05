from openerp import models, fields, api
from ..connector.backend import prestashop
from ..unit.adapter import PrestaShopAdapter
from ..unit.binder import PrestaShopBinder
from ..unit.exporter import (PrestaShopExporter,
                             PrestaShopBatchExporter)
from openerp.addons.connector.unit.mapper import (ExportMapper,
                                                  only_create,
                                                  mapping)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    prestashop_bind_ids = fields.One2many(
        string = "PrestaShop Bindings",
        comodel_name = 'prestashop.product.template',
        inverse_name = 'odoo_id',
    )
    in_store = fields.Boolean(
        string = "In Store?",
        index = True,
    )

    #TODO: override copy so bind_ids don't copy


class PrestaShopProductTemplate(models.Model):
    _name = 'prestashop.product.template'
    _description = "Prestashop Product Template Binding"
    _inherit = 'prestashop.binding'
    _inherits = {'product.template': 'odoo_id'}

    odoo_id = fields.Many2one(
        string = "Product",
        comodel_name = 'product.template',
        required = True,
        ondelete = 'cascade',
    )

@prestashop
class ProductTemplateAdapter(PrestaShopAdapter):
    _model_name = 'prestashop.product.template'
    _prestashop_model = 'products'

@prestashop
class ProductTemplateBinder(PrestaShopBinder):
    _model_name = 'prestashop.product.template'

@prestashop
class ProductTemplateExporter(PrestaShopExporter):
    _model_name = 'prestashop.product.template'

@prestashop
class ProductTemplateBatchExporter(PrestaShopBatchExporter):
    _model_name = 'prestashop.product.template'
    
@prestashop
class ProductTemplateExportMapper(ExportMapper):
    _model_name = 'prestashop.product.template'

    direct = [
        ('id', 'id'),
        ('name', 'name'),
        ('list_price', 'price'),
        ('default_code', 'reference'),
    ]

    @only_create
    @mapping
    def blank_id(self, record):
        return {'id': ''}

"""    
@prestashop
class ProductInventoryAdapter(PrestaShopAdapter):
    _model_name = '_import_stock_available'
    _prestashop_model = 'stock_availables'
    _export_node_name = 'stock_available'

    def get(self, options=None):
        api = self.connect()
        return api.get(self._prestashop_model, options=options)

    def export_quantity(self, filters, quantity):
        self.export_quantity_url(
            self.backend_record.location,
            self.backend_record.key,
            filters,
            quantity
        )

        shop_ids = self.session.search('prestashop.shop', [
            ('backend_id', '=', self.backend_record.id),
            ('default_url', '!=', False),
        ])
        shops = self.session.browse('prestashop.shop', shop_ids)
        for shop in shops:
            self.export_quantity_url(
                '%s/api' % shop.default_url,
                self.backend_record.key,
                filters,
                quantity
            )

    def export_quantity_url(self, url, key, filters, quantity):
        api = PrestaShopWebServiceDict(url, key)
        response = api.search(self._prestashop_model, filters)
        for stock_id in response:
            res = api.get(self._prestashop_model, stock_id)
            first_key = res.keys()[0]
            stock = res[first_key]
            stock['quantity'] = int(quantity)
            try:
                api.edit(self._prestashop_model, {
                    self._export_node_name: stock
                })
            except ElementTree.ParseError:
                pass


# fields which should not trigger an export of the products
# but an export of their inventory
INVENTORY_FIELDS = ('quantity',)


@on_record_write(model_names='prestashop.template.product')
def prestashop_product_stock_updated(session, model_name, record_id,
                                     fields=None):
    if session.context.get('connector_no_export'):
        return
    inventory_fields = list(set(fields).intersection(INVENTORY_FIELDS))
    if inventory_fields:
        export_inventory.delay(session, model_name,
                               record_id, fields=inventory_fields,
                               priority=20)

@job
def export_inventory(session, model_name, record_id, fields=None):
    "" Export the inventory configuration and quantity of a product. ""
    product = session.browse(model_name, record_id)
    backend_id = product.backend_id.id
    env = get_environment(session, model_name, backend_id)
    inventory_exporter = env.get_connector_unit(ProductInventoryExport)
    return inventory_exporter.run(record_id, fields)
"""
