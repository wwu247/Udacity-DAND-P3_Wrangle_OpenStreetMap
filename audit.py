import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "richmond_virginia.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Mapping for streets
expected = ["Boulevard", "Court", "West", "North", "South", "Road", "Street", "Way", "Circle", "Highway", 
"Drive", "Turnpike", "Lane", "Place", "Parkway", "Loop", "Alley", "Village", "Avenue"]

mapping = { "St": "Street",
            "street": "Street",
            "Ave": "Avenue",
            "Rd": "Road",
            "Dr": "Drive",
            "Tnpk": "Turnpike",
            "Pkwy": "Parkway",
            "Pky": "Parkway",
            "W.": "West",
            "W": "West",
            "N.": "North",
            "N": "North",
            "S.": "South",
            "Ct": "Court"
            }


# Mapping for cities
exp_cities = ["Richmond", "Glen Allen"]

map_cities = { "richmond": "Richmond",
               "Richmond City": "Richmond",
               "glen Allen": "Glen Allen"
                }


# Mapping for state name
exp_states = ["VA"]

map_states = { "Virginia": "VA" }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")

def is_state_name(elem):
    return (elem.attrib['k'] == "addr:state")

def update_street(name, mapping):
# iterate over each word in street name to correct street name
    words = name.split(" ")

    for w in range(len(words)):
        if words[w] in mapping:
            words[w] = mapping[words[w]] 
            name = " ".join(words)
    return name

def update_name(name, mapping):
# correct state and city names
    if name in mapping.keys():
        name = mapping[name]
    return name

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                
                # use 'if is_street_name()' function to determine if the attribute matches
                if is_street_name(tag):              
                    tag.attrib['v'] = update_street(tag.attrib['v'], mapping)

                if is_city_name(tag):
                    tag.attrib['v'] = update_name(tag.attrib['v'], map_cities)

                if is_state_name(tag):
                    tag.attrib['v'] = update_name(tag.attrib['v'], map_states)

    osm_file.close()
    return street_types


pprint.pprint(audit(OSMFILE))