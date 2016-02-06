import element_tree as ElementTree


def getNode(xml, name):
    element = ElementTree.fromstring(xml)
    return element.find(name).text

def setNode(xml, name, value):
    element = ElementTree.fromstring(xml)
    element.find(name).text = str(value)
    return ElementTree.tostring(element)

def data2xml(data, schema):
    element = ElementTree.fromstring(schema)
    
    for k, v in data.iteritems():
        element.find(k).text = str(v)
    
    return ElementTree.tostring(element)

#broken!!
def xml2data(xml):
    element = ElementTree.fromstring(xml)
    data = {}
    
    for child in element[0]:
        data[child.tag] = child.text
    
    return data
