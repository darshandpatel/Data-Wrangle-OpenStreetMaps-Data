import csv
import pprint
import re

INPUT_FILE = '/Users/Darshan/Documents/Data-Wrangle-OpenStreetMaps-Data/data/autos.csv'
OUTPUT_GOOD = '/Users/Darshan/Documents/Data-Wrangle-OpenStreetMaps-Data/data/autos-valid.csv'
OUTPUT_BAD = '/Users/Darshan/Documents/Data-Wrangle-OpenStreetMaps-Data/data/FIXME-autos.csv'
year_re = re.compile(r'\d{4}', re.IGNORECASE)

def process_file(input_file, output_good, output_bad):
    # store data into lists for output
    data_good = []
    data_bad = []
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        good_count = 0
        bad_count = 0
        for row in reader:
            # validate URI value
            if row['URI'].find("dbpedia.org") < 0:
                continue

            ps_year = row['productionStartYear'][:4]
            try: # use try/except to filter valid items
                ps_year = int(ps_year)
                row['productionStartYear'] = ps_year
                if (ps_year >= 1886) and (ps_year <= 2014):
                    good_count += 1
                    data_good.append(row)
                else:
                    data_bad.append(row)
                    bad_count += 1
            except ValueError: # non-numeric strings caught by exception
                if ps_year == 'NULL':
                    bad_count += 1
                    data_bad.append(row)
    print 'good count',good_count
    print 'bad count',bad_count
    # Write processed data to output files
    with open(output_good, "w") as good:
        writer = csv.DictWriter(good, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in data_good:
            writer.writerow(row)

    with open(output_bad, "w") as bad:
        writer = csv.DictWriter(bad, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in data_bad:
            writer.writerow(row)

def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()