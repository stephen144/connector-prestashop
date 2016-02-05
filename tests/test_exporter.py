import unittest
from openerp.addons.connector.session import ConnectorSession
from ..unit.exporter import (
    PrestaShopExporter,
    export_record,
)

class TestExporter(unittest.TestCase):

    def setUp(self):
        self.session = ConnectorSession(
            self.env.cr,
            self.env.uid,
            context = self.env.context,
        )

    def test_export_record(self):
        
