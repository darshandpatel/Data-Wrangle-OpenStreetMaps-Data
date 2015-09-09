#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pprint
import re
import xml.etree.cElementTree as ET
import time
import info
import codecs
import json
"""
This code Wrangles the boston openstreetmap data and transforms the shape of the data into
the JSON and adds into the mongodb collection.

JSON Example :
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

"""

# Regular Expression
problem_chars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addr_start_chars = re.compile(r'^addr:')
address_expr = re.compile(r'^address$')
address_street_chars = re.compile(r'^addr:street')
tag_property = re.compile(r'^.*:.*')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

"""
This function examines the various XML tag and their elements of Boston OSM file and converts
them into appropriate JSON object
"""


def shape_element(element):

    # All the properties of tag should be added into node dictionary
    node = {}

    # All the properties related to creation and modification timing should be added to
    # created dictionary
    created = {}

    if element.tag == "node" or element.tag == "way" or element.tag == "relation":

        # latitude
        lat = None
        # longitude
        lon = None
        # position = [latitude,longitude]
        pos = None

        node["type"] = element.tag

        # Scan all the attribute of current tag and add them into node dictionary

        for attrib in element.attrib:

            attrib_value = element.get(attrib)

            if attrib in CREATED:
                created[attrib] = attrib_value
            elif attrib == 'lat':
                lat = float(attrib_value)
                #pos.append(float(attrib_value))
            elif attrib == 'lon':
                lon = float(attrib_value)
                #pos.append(float(attrib_value))
            else:
                node[attrib] = attrib_value

        if lat is not None and lon is not None:
            pos = [lat,lon]

        # All the address related information should be added to address dictionary
        address = {}
        # In "way" and "relation" tag, all the mentioned/referred tag should be
        # added into node_refs list
        node_refs = []
        # All the members of "relation" tag should be added into members list
        members = []

        # Scan all the child tag element of current tag.
        for sub_tag in element:

            #print "{0} tag {1}".format("Inside for loop",sub_tag.tag)

            if sub_tag.tag == "tag":

                k_value = sub_tag.get("k")
                v_value = sub_tag.get("v")

                if problem_chars.match(k_value):
                    #print 'Problematic'
                    continue
                elif address_expr.match(k_value):
                    #23 Leonard Street, Boston MA 02122 -> split into [(23 Leonard Street),(Boston MA 02122)]
                    address_parts = v_value.split(',')
                    if len(address_parts) == 2:

                        street = address_parts[0].strip().split(' ')
                        if len(street) >= 2:
                            if street[0].isdigit():
                                address["housenumber"] = street[0]
                                address["street"] = ' '.join(street[1:])
                        elif len(street) == 1:
                            address["street"] = street

                        second_part = address_parts[1].strip().split(' ')
                        if len(second_part) == 3:
                            address["city"],address["state"],address["postcode"] = second_part
                        else:
                            print "Bad second address part :{0}".format(second_part)
                    else:
                        print "Bad address :{0}".format(v_value)
                elif addr_start_chars.match(k_value):

                    if re.match(r'^.*:.*:.*',k_value):
                        #print '{0} {1}'.format("Check this one",k_value)
                        continue
                    elif address_street_chars.match(k_value):
                        property = k_value.replace("addr:","")
                        address[property] = v_value
                    else:
                        property = k_value.split(":")
                        address[property[1]] = v_value
                #elif tag_property.match(k_value):
                #    address[k_value] = v_value
                #elif element.tag == "relation":
                else:
                    node[k_value] = v_value

            elif sub_tag.tag == 'nd':
                node_refs.append(sub_tag.get("ref"))

            elif sub_tag.tag == 'member':
                member = {}
                for attrib in sub_tag.attrib:
                    attrib_value = sub_tag.get(attrib)
                    if attrib_value != "":
                        member[attrib] = attrib_value
                if member:
                    members.append(member)

        if created:
            node["created"] = created
        if address:
            node["address"] = address
        if node_refs:
            node["node_refs"] = node_refs
        if pos:
            node["pos"] = pos
        if members:
            node["members"] = members

        return node

def process_map(file_in, pretty = False):

    #file_out = "{0}.json".format(file_in)


    client = info.getMongoClient("localhost:27017")
    db = client.example
    db.test.drop()


    #with codecs.open(file_out, "w") as fo:

    context = iter(ET.iterparse(file_in, events=('start', 'end')))
    _, root = next(context) # get root element
    for event, element in context:
        if event == 'end':
            el = shape_element(element)
            if el:
                db.test.insert(el)
                '''
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
                '''
            root.clear() # preserve memory


if __name__ == "__main__":
    start_time = time.time()
    process_map('/Users/Darshan/Documents/Data-Wrangle-OpenStreetMaps-Data/data/example.osm', False)
    print("--- %s seconds ---" % (time.time() - start_time))
