from openerp import models, fields, api
from openerp.addons.connector.unit.synchronizer import Exporter


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    prestashop_bind_ids = fields.One2many(
        comodel_name = 'prestashop.product.template',
        inverse_name = 'odoo_id',
        string = "PrestaShop Bindings",
    )

    #override copy so bind_ids don't copy?


class PrestashopProductTemplate(models.Model):
    """

    """
    
    _name = 'prestashop.product.template'
    _description = "Prestashop Product Template Binding"
    _inherit = 'prestashop.binding'
    _inherits = {'product.product': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name = 'product.template',
        string = "Product",
        required = True,
        ondelete = 'cascade',
    )


@prestashop
class ProductTemplateExporter(Exporter):
    _model_name = 'prestashop.product.template'

    def get_filter(self, product):
        binder = self.get_binder_for_model()
        prestashop_id = binder.to_backend(product.id)
        return {
            'filter[id_product]': prestashop_id,
            'filter[id_product_attribute]': 0
        }

    def run(self, binding_id):
        """ Export the product template to Prestashop """
        
        product = self.model.browse(binding_id)
        prestashop_id = self.binder.to_backend(product.id)
        data = self._get_data(product)
        self.backend_adapter.export_quantity(
            None,
            int(product.quantity),
        )
        """
        adapter = self.get_connector_unit_for_model(
            GenericAdapter, '_import_stock_available'
        )
        filter = self.get_filter(product)
        adapter.export_quantity(filter, int(product.quantity))
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
            self.backend_record.webservice_key,
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
                self.backend_record.webservice_key,
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


@on_record_write(model_names=[
    'prestashop.product.product',
])
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
    """ Export the inventory configuration and quantity of a product. """
    product = session.browse(model_name, record_id)
    backend_id = product.backend_id.id
    env = get_environment(session, model_name, backend_id)
    inventory_exporter = env.get_connector_unit(ProductInventoryExport)
    return inventory_exporter.run(record_id, fields)
