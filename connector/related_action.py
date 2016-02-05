import functools
from openerp.addons.connector import related_action
from ..unit.binder import PrestaShopBinder


unwrap_binding = functools.partial(related_action.unwrap_binding,
                                   binder_class=PrestaShopBinder)
