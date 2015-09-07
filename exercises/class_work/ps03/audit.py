#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a
SET of the types that can be found in the field. e.g.
{"field1: set([float, int, str]),
 "field2: set([str]),
  ....
}

All the data initially is a string, so you have to do some checks on the values
first.
"""
import codecs
import csv
import json
import pprint
import re
import types

CITIES = '/Users/Darshan/Documents/Data-Wrangle-OpenStreetMaps-Data/data/cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal",
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long",
          "areaLand", "areaMetro", "areaUrban"]
str_re = re.compile('[a-zA-Z]',re.IGNORECASE)
list_re = re.compile('^{',re.IGNORECASE)
int_re = re.compile('[0-9]*',re.IGNORECASE)

def audit_file(filename, fields):
    fieldtypes = {}
    # YOUR CODE HERE
    file_pointer = open(filename,'r')
    reader = csv.DictReader(file_pointer)
    header = next(reader)
    header = next(reader)
    header = next(reader)
    for row in reader:
        print row['name']
        for field in FIELDS:
            if field == 'postalCode':
                print row[field]
            if 'NULL' == row[field] or row[field] == '':
                found_type = types.NoneType
            elif list_re.match(row[field]):
                found_type = types.ListType
            else:
                try:
                    dummy = int(row[field])
                    found_type = types.IntType
                except:
                    try:
                        dummy = float(row[field])
                        found_type = types.FloatType
                    except:
                        found_type = types.StringType
            if field in fieldtypes:
                field_set = set()
                field_set.add(found_type)
                fieldtypes[field] = fieldtypes[field].union(field_set)
            else:
                field_set = set()
                field_set.add(found_type)
                fieldtypes[field] = field_set
    file_pointer.close()
    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])

if __name__ == "__main__":
    test()
