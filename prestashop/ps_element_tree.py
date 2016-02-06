from xml.etree import ElementTree


class PrestaShopElement(ElementTree.Element):

    def _find(element, match):
        return super(PrestaShopElement, element).find(match)
    
    def find(self, match):
        
        element = self[0]._find(match)

        if len(element) == 0:
            return element

        if element._find('language') is not None:
            return element._find('language')

        return None


class _PrestaShopElementFactory(object):
    
    def __call__(self, tag, attrib={}, **extra):
        return PrestaShopElement(tag, attrib, **extra)


element_factory = _PrestaShopElementFactory()
_tree_builder = ElementTree.TreeBuilder(element_factory)
_parser = ElementTree.XMLParser(target=_tree_builder)
    

def fromstring(text):
    _parser.feed(text)
    return _parser.close() 


def tostring(element):
    return ElementTree.tostring(element, 'utf-8')
