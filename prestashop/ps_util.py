import ..prestashop.ps_element_tree as ElementTree


def data2xml(data, schema):
    element = ElementTree.fromstring(schema)
    
    for k, v in data.iteritems():
        element.find(k).text = str(v)
    
    xml = ElementTree.tostring(element)
    return xml

#broken
def xml2data(xml):
    element = ElementTree.fromstring(xml)
    data = {}
    
    for child in element[0]:
        data[child.tag] = child.text
    
    return data
