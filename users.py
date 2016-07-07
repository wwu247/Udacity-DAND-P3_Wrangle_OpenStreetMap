import xml.etree.cElementTree as ET
import pprint
import re


def get_user(element):
    if element.attrib.get('uid') is not None:
        return element.attrib["uid"]


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        u = get_user(element)
        if u is not None:
            users.add(u)
        pass
   
    return users


u = process_map("richmond_virginia.osm")
pprint.pprint(u)
print len(u)