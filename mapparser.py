import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):
        # YOUR CODE HERE
    tag = {}
    
    for event, elem in ET.iterparse(filename):
        if elem.tag not in tag.keys():
            tag[elem.tag] = 1
        else:
            tag[elem.tag] += 1

    return tag

pprint.pprint(count_tags("richmond_virginia.osm"))