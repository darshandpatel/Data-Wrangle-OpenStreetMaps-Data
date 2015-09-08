"""
This file audits the Boston Collection for unexpected street types to the appropriate ones in
the expected list.

Apart from that, update_name function actually fix the unexpected street types in Boston
Collection.
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

collection = "boston"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
postcode_re = re.compile(r'^[0-9]{5}$')

# Expected street types
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons","Highway","Way","Artery","Broadway","Center","Terrace","Circle","Park"]

# MAPPING VARIABLE
mapping = { "Ave" : "Avenue",
            "Ave." : "Avenue",
            "ave" : "Avenue",
            "Cir" : "Circle",
            "Ct" : "Court",
            "Hwy" : "Highway",
            "Pkwy" : "Parkway",
            "Rd." : "Road",
            "Rd" : "Road",
            "rd." : "Road",
            "St": "Street",
            "St.": "Street",
            "St," : "Street",
            "st" : "Street",
            "ST" : "Street",
            "Street." : "Street",
            "street" : "Street",
            "Sq." : "Square"}


# This function audits the street type in addresses
def street_audit():

    results = db.boston.find({"address.street" : { "$exists" : 1}},
                            { "id" : 1, "address.street" : 1})

    street_types = defaultdict(set)

    for result in results:
        street_name = result["address"]["street"]
        m = street_type_re.search(street_name)
        if m:
            street_type = m.group()
            if street_type not in expected:
                # Update the street type if a street type does not exist in expected
                # street type list and exists in mapping dictionary
                if street_type in mapping.keys():
                    street_name = street_name.replace(street_type,mapping[street_type])
                    db.boston.update_one({"id": result["id"]},
                                                     { "$set" : {
                                                         "address.street" : street_name
                                                        }})
                else:
                    street_types[street_type].add(street_name)
    pprint.pprint(dict(street_types))


# This function audits the postcode in addresses
def postcode_audit():

    results = db.boston.find({"address.postcode" : { "$exists" : 1}},
                            { "id" : 1, "address.postcode" : 1})

    for result in results:
        postcode = result["address"]["postcode"]
        if not postcode_re.match(postcode):
            print postcode


# This function audits the phone
def phone_audit():

    results = db.boston.find({"phone" : { "$exists" : 1}},
                            { "id" : 1, "phone" : 1})

    for result in results:
        phone = result["phone"]
        print phone


if __name__ == '__main__':

    from pymongo import MongoClient
    client = MongoClient("localhost:27017")
    db = client.openstreetmap

    '''
    query = [{"address.street" : { "$exists" : 1}},
             { "id" : 1, "address.street" : 1}]
    '''

    street_audit()
    #postcode_audit()
    #phone_audit()

    #print results.count()

    '''
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
    '''