"""
class ProductCategory(models.Model):
    _inherit = 'product.category'

    prestashop_bind_ids = fields.One2many(
        comodel_name = 'prestashop.product.category',
        inverse_name = 'odoo_id',
        string = "PrestaShop Bindings",
    )


class PrestashopProductCategory(models.Model):
    """

    """
    
    _name = 'prestashop.product.category'
    _description = "Prestashop Product Category Binding"
    _inherit = 'prestashop.binding'
    _inherits = {'product.category': 'odoo_id'}

    odoo_id = fields.many2one(
        comodel_name = 'product.category',
        string = "Product Category",
        required = True,
        ondelete = 'cascade',
    )
"""
