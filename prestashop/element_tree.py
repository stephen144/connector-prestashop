from xml.etree import ElementTree


def _attr_e(e, name):
    if name == 'text':
        if len(e) == 1 and e[0].tag == 'language':
            return e[0]
        
    return e

def _find_e(e):
    if len(e) == 1 and e.tag == 'prestashop':
        return e[0]
    else:
        return e


class PrestaShopElement(ElementTree.Element):

    def __getattribute__(self, name):
        e = _attr_e(self, name)
        return super(PrestaShopElement, e).__getattribute__(name)

    def __setattr__(self, name, value):
        e = _attr_e(self, name)
        super(PrestaShopElement, e).__setattr__(name, value)

    def find(self, match):
        e = _find_e(self)
        super(PrestaShopElement, e).find(match)

    def findall(self, match):
        e = _find_e(self)
        super(PrestaShopElement, e).findall(match)

class _PrestaShopElementFactory(object):
    
    def __call__(self, tag, attrib={}, **extra):
        return PrestaShopElement(tag, attrib, **extra)


element_factory = _PrestaShopElementFactory()
tree_builder = ElementTree.TreeBuilder(element_factory)


def fromstring(text):
    parser = ElementTree.XMLParser(target=tree_builder)
    parser.feed(text)
    return parser.close()

def tostring(element):
    return ElementTree.tostring(element, 'utf-8')
