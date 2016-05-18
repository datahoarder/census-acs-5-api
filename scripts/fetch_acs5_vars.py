"""
fetch_acs5_vars.py

This script fetches the master list of variables (20+MB) for the Census
ACS 5-year survey and saves a copy as JSON and as CSV. The CSV version
is slightly more organized.

The variables file is only for reference. No other script references them.

More information about ACS5 can be found here:
http://www.census.gov/data/developers/data-sets/acs-survey-5-year-data.html
"""

from os.path import join
from os import makedirs
import csv
import json
import requests


DATA_URL = 'http://api.census.gov/data/2014/acs5/variables.json'
DATA_DIR = join('data', 'fetched')
makedirs(DATA_DIR, exist_ok=True)
DEST_JSONNAME = join(DATA_DIR, 'acs5-variables.json')
DEST_CSVNAME = join(DATA_DIR, 'acs5-variables.csv')
VARIABLE_FIELDNAMES = ['name', 'concept', 'label', 'predicateType']

if __name__ == '__main__':

    # fetch the data
    print("Fetching data at", DATA_URL)
    resp = requests.get(DATA_URL)
    data = json.loads(resp.text) # deserialize
    # write a JSON version of it
    with open(DEST_JSONNAME, 'w') as wf:
        print("Saving to", DEST_JSONNAME)
        # ... and then serialize, because
        # we want the pretty indentation
        json.dump(data, wf, indent=2)

    # prepare the CSV file
    destfile = open(DEST_CSVNAME, 'w')
    destcsv = csv.DictWriter(destfile, fieldnames=VARIABLE_FIELDNAMES,
                               extrasaction='ignore')
    print("Saving to", DEST_CSVNAME)
    destcsv.writeheader()

    # let's sort them in order of variable name, i.e. the key in
    # each key-val pair
    ditems = sorted(data['variables'].items(), key=lambda x: x[0])
    for vname, vdict in ditems:
        vdict['name'] = vname
        destcsv.writerow(vdict)


    destfile.close()
