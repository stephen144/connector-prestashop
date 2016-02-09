import element_tree as ElementTree


def getNode(xml, name):
    e = ElementTree.fromstring(xml)
    return e.find(name).text

def setNode(xml, name, value):
    e = ElementTree.fromstring(xml)
    e.find(name).text = str(value)
    return ElementTree.tostring(e)

def data2xml(data, schema):
    e = ElementTree.fromstring(schema)
    for k, v in data.iteritems():
        e.find(k).text = str(v)
    return ElementTree.tostring(e)

def xml2data(xml):
    e = ElementTree.fromstring(xml)
    children = e.findall("*")
    data = {}

    for child in children:
        data[child.tag] = child.text
    
    return data
