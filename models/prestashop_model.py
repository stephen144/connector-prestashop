from openerp import models, fields, api
from openerp.addons.connector.session import ConnectorSession
from ..unit.exporter import export_batch


class PrestaShopBackend(models.Model):
    _name = 'prestashop.backend'
    _description = 'PrestaShop Backend'
    _inherit = 'connector.backend'
    _backend_type = 'prestashop'

    version = fields.Selection(
        selection = '_select_versions',
        required = True,
    )
    location = fields.Char(required=True)
    key = fields.Char(required=True)

    @api.model
    def _select_versions(self):
        return [('1.6.1.4', '1.6.1.4')]

    @api.multi
    def export_products(self):
        self._export_model('prestashop.product.template')
    
    @api.multi
    def _export_model(self, model):
        session = ConnectorSession(
            self.env.cr,
            self.env.uid,
            context = self.env.context,
        )
        self.ensure_one()
        export_batch.delay(session, model, self.id)

        
class PrestaShopBinding(models.AbstractModel):
    _name = 'prestashop.binding'
    _description = 'PrestaShop Binding (abstract)'
    _inherit = 'external.binding'

    backend_id = fields.Many2one(
        comodel_name = 'prestashop.backend',
        string = "PrestaShop Backend",
        required = True,
        ondelete = 'restrict',
    )
    prestashop_id = fields.Integer(string="PrestaShop ID")

    _sql_constraints = [
        ('prestashop_uniq', 'unique(backend_id, prestashop_id)',
         'A binding already exists with the same Prestashop ID.'),
    ]
