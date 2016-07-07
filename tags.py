import xml.etree.cElementTree as ET
import pprint
import re


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    
    if (element.tag == "tag"):
        lower_re = lower.search(element.attrib['k'])
        lower_colon_re = lower_colon.search(element.attrib['k'])
        problemchars_re = problemchars.search(element.attrib['k'])
        if lower_re:
            keys["lower"] +=1
        elif lower_colon_re:
            keys["lower_colon"] +=1
        elif problemchars_re:
            keys ["problemchars"] +=1
        else:
            keys ["other"] +=1
        pass
        
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

pprint.pprint(process_map("richmond_virginia.osm"))