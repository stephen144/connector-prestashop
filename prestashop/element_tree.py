from xml.etree import ElementTree


def _attribute_e(e, name):
    def skip_root(e):
        if len(e) == 1 and e.tag == 'prestashop':
            return e[0]
        else:
            return e

    if name == 'find':
        return skip_root(e)
    if name == 'findall':
        return skip_root(e)
    if name == 'text':
        if len(e) == 1 and e[0].tag == 'language':
            return e[0]

    return e



class PrestaShopElement(ElementTree.Element):

    @property
    def data(self):
        data = {}
        for child in self.findall('*'):
            data[child.tag] = child.text
        return data

    @data.setter
    def data(self, data):
        for k, v in data.iteritems():
            self.find(k).text = str(v)
    
    def __getattribute__(self, name):
        e = super(PrestaShopElement, self)
        
        if hasattr(super(PrestaShopElement, e), name):
            e = _attribute_e(e, name)
            return e.__getattribute__(name)
        else:
            raise AttributeError

    def __getattr__(self, name):
        e = self.find(name)
        if e is None:
            raise AttributeError
        else:
            return e.text
        
    def __setattr__(self, name, value):
        e = super(PrestaShopElement, self)
        
        if hasattr(e, name):
            e = _attribute_e(e, name)
            e.__setattr__(name, value)
        elif self.find(name) is not None:
            self.find(name).text = str(value)
        else:
            e.__setattr__(name, value)

    
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


class PrestaShopXML(object):

    def __init__(self, xml):
        self.xml = xml

    @property
    def element(self):
        #import pdb; pdb.set_trace()
        return fromstring(self.xml)

    @element.setter
    def element(self, value):
        self.xml = tostring(value)

    @property
    def children(self):
        return self.element.findall('*')
      
    def __repr__(self):
        return self.xml

    def __getattr__(self, name):
        return self.element.find(name).text

    def __setattr__(self, name, value):
        if name == 'xml':
            return
        
        if name == 'element' or name == 'data':
            object.__setattr__(self, name, value)
        else:
            e = self.element
            e.find(name).text = str(value)
            self.element = e
