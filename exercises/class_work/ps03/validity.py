"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in range, as described above,
  write that line to the output_good file
- if the value of the field is not a valid year,
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint
import re

INPUT_FILE = '/Users/Darshan/Documents/Data-Wrangle-OpenStreetMaps-Data/data/autos.csv'
OUTPUT_GOOD = '/Users/Darshan/Documents/Data-Wrangle-OpenStreetMaps-Data/data/autos-valid.csv'
OUTPUT_BAD = '/Users/Darshan/Documents/Data-Wrangle-OpenStreetMaps-Data/data/FIXME-autos.csv'
year_re = re.compile(r'\d{4}', re.IGNORECASE)

def process_file(input_file, output_good, output_bad):

    good_data =[]
    bad_data = []
    good_count = 0
    bad_count = 0
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        for row in reader:
            if "dbpedia.org" in row['URI']:
                year_found = year_re.search(row['productionStartYear'])

                if year_found:
                    year = int(year_found.group())
                    row['productionStartYear'] = year
                    if (year <= 2014) and (year >= 1886):
                        good_count += 1
                        good_data.append(row)
                    else:
                        bad_count += 1
                        bad_data.append(row)
                else:
                    bad_count += 1
                    bad_data.append(row)

        #COMPLETE THIS FUNCTION
    YOURDATA = []

    print 'good count',good_count
    print 'bad count',bad_count
    # This is just an example on how you can use csv.DictWriter
    # Remember that you have to output 2 files
    with open(output_good, "w") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in good_data:
            writer.writerow(row)

    with open(output_bad, "w") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in bad_data:
            writer.writerow(row)


def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()