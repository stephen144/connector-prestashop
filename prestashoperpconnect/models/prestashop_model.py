from openerp import models, fields, api


class PrestashopBackend(models.Model):
    _name = 'prestashop.backend'
    _doc = 'Prestashop Backend'
    _inherit = 'connector.backend'
    _backend_type = 'prestashop'

    version = fields.Selection(selection='_select_versions')
    location = fields.Char()
    webservice_key = fields.Char()

    @api.model
    def _select_versions(self):
        """ Available versions

        Can be inherited to add custom versions.
        """
        return [('1.6.0.11', '1.6.0.11')]


class PrestashopBinding(models.AbstractModel):
    """

    """
    
    _name = 'prestashop.binding'
    _inherit = 'external.binding'
    _description = 'PrestaShop Binding (abstract)'

    #
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
