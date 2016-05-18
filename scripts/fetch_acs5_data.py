"""
fetch_acs_data.py

This script parses data/acs5-var-lookups.csv to get a list
of Census ACS-5 variables to collect. Then, for a series of jurisdictions,
including the entire United States, each state, every zip code,
every county, and every congressional district, it collects those variables
across 2010 and 2014.

More information about ACS5 can be found here:
http://www.census.gov/data/developers/data-sets/acs-survey-5-year-data.html

Examples can be found here:
http://api.census.gov/data/2014/acs5/examples.html
"""

import csv
import requests
from copy import copy
from os.path import join, exists
from os import makedirs
DATA_DIR = 'data'
FETCHED_DATA_DIR = join(DATA_DIR, 'fetched')
CENSUS_VAR_FILENAME = join(DATA_DIR, 'acs5-var-lookups.csv')

ALL_GEOS = ['us', 'state', 'county', 'congressional+district', 'zip+code+tabulation+area']
ALL_YEARS = [2009, 2010, 2011, 2012, 2013, 2014]
LIMITED_GEOS = ['zip+code+tabulation+area']
LIMITED_YEARS = [2011, 2012, 2013, 2014]

with open(CENSUS_VAR_FILENAME) as f:
    CENSUS_VARS = list(csv.DictReader(f))
    CENSUS_VARNAMES = [x['name'] for x in CENSUS_VARS]

CENSUS_API_KEY = open('mycensuskey.txt').read().strip()

ACS_5_ENDPOINT_URL = 'http://api.census.gov/data/{year}/acs5'
DEFAULT_PARAMS = {
    'get': ','.join(['NAME'] + CENSUS_VARNAMES),
    'key': CENSUS_API_KEY
}

# Let's start with the


for geoname in ALL_GEOS:
    years = LIMITED_YEARS if geoname in LIMITED_GEOS else ALL_YEARS
    for year in years:
        dest_dir = join(FETCHED_DATA_DIR, geoname)
        dest_fname = join(dest_dir, '{0}.json'.format(year))
        if exists(dest_fname):
            print("Already downloaded", dest_fname)
        else:
            print("Downloading", dest_fname)

        # fname = join()
        # myparams = copy(DEFAULT_PARAMS)
        # myparams['for'] = geo + ':*' # e.g. for=county:*
        # requests.get()



# # let's get the data for year

# ?for=zip+code+tabulation+area:52240,94025&get=B01003_001E,B11011_001E,B11011_002E,B11011_004E'
