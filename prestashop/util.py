def populate(e, data):
    for k, v in data.iteritems():
        
        path = "./*[1]/{}/language".format(k)
        if e.find(path) is not None:
            e.find(path).text = str(v)
            continue
        
        path = "./*[1]/{}".format(k)
        if e.find(path) is not None:
            e.find(path).text = str(v)

def todict(e):
    d = {}
    children = e.findall('./*[1]/*')
    
    for c in children:
        if c.find('./language') is not None:
            d[c.tag] = c.find('./language').text
        else:
            d[c.tag] = c.text

    return d
