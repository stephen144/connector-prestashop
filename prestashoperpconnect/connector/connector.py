from openerp.addons.connector.connector import ConnectorEnvironment
    

def get_environment(session, model, backend_id):
    backend = session.env['prestashop.backend'].browse(backend_id)
    return ConnectorEnvironment(backend, session, model)
