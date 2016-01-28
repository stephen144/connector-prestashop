from prestapyt import (
    PrestaShopWebService,
    PrestaShopWebServiceDict,
    PrestaShopWebServiceError,
)

from xml.etree import ElementTree
from xml.dom import minidom


ps = PrestaShopWebService('http://winona/prestashop/api',
                          'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L')
#ps.debug = True

psd = PrestaShopWebServiceDict('http://winona/prestashop/api',
                               'E3P9JC4E5NRJ63ZZYJNKG4IPWGDPEG4L')
#psd.debug = True

def pp(elem):
    return ElementTree.tostring(elem, 'utf-8')

def pprint(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
