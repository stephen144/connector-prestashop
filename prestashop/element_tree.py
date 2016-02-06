from xml.etree import ElementTree


class PrestaShopElement(ElementTree.Element):

    def _e(self):
        if len(self) > 0:
            return self[0]
        else:
            return self      
    
    def __getattribute__(self, name):
        e = self._e()
        return super(PrestaShopElement, e).__getattribute__(name)

    def __setattr__(self, name, value):
        e = self._e()
        super(PrestaShopElement, e).__setattr__(name, value)
    
    def find(self, match):
        e = self._e()
        return super(PrestaShopElement, e).find(match)


class _PrestaShopElementFactory(object):
    
    def __call__(self, tag, attrib={}, **extra):
        return PrestaShopElement(tag, attrib, **extra)


element_factory = _PrestaShopElementFactory()
tree_builder = ElementTree.TreeBuilder(element_factory)
#_parser = ElementTree.XMLParser(target=_tree_builder)
    

def fromstring(text):
    parser = ElementTree.XMLParser(target=tree_builder)
    parser.feed(text)
    return parser.close() 


def tostring(element):
    return ElementTree.tostring(element, 'utf-8')
