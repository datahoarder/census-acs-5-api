"""
reads from data/compiled/acs5-compiled-percentages.csv
For each geography, creates:
    data/wrangled/acs-delta-{geo}-{year1}-{year2}.json

These JSON files are meant to be ready-to-import into an app and contains
useful calculations, such as the change between each variable from
year2 to year1

Caution: Takes a very long time to run
"""

from collections import OrderedDict
from os.path import join
from os import makedirs
import csv
import json

CURRENT_YEAR = 2014
PAST_YEAR = 2011

DATA_DIR = 'data'
SRC_DATA_DIR = join(DATA_DIR, 'compiled')
SRC_FILENAME =  join(SRC_DATA_DIR, 'acs5-compiled-percentages.csv')
DEST_DATA_DIR = join(DATA_DIR, 'wrangled', 'acs5-{0}-{1}'.format(PAST_YEAR, CURRENT_YEAR))
makedirs(DEST_DATA_DIR, exist_ok=True)


ALL_GEOS = ['us', 'state', 'county', 'congressional+district'] # don't do zips for now...they too big, 'zip+code+tabulation+area']
IGNORE_HEADERS = ['name', 'geo', 'slug', 'year']


# open the source data
print("Reading", SRC_FILENAME)
with open(SRC_FILENAME, 'r') as rf:
    datarows = list(csv.DictReader(rf))
    headers = list(datarows[0].keys())
    data_headers = list(set(headers) - set(IGNORE_HEADERS))

print("Cleaning up the data")
# clean up the file
for r in datarows:
    r['year'] = int(r['year'])
    if r['year'] != CURRENT_YEAR and r['year'] != PAST_YEAR:
        pass
    else:
        for h in data_headers:
            if '.' in r[h]: # make it a float
                r[h] = float(r[h])
            elif '' == r[h]:
                r[h] = None
            else:
                r[h] = int(r[h])



for geoname in ALL_GEOS:
    print("On geoname", geoname)
    entities = []
    # get a list of all the relevant data rows
    georows = [row for row in datarows if row['geo'] == geoname]
    uslugs = set([row['slug'] for row in georows])
    # get a list of all unique slugs
    for i, slug in enumerate(uslugs):
        if i % 1001 == 0:
            print("On slug named:", slug, ' -- ', i, "out of", len(uslugs), "total slugs")
        # print("\tAggregating", slug)
        current_row = next((r for r in georows if r['year'] == CURRENT_YEAR and r['slug'] == slug), None)
        past_row = next((r for r in georows if r['year'] == PAST_YEAR and r['slug'] == slug), None)

        # rare cases in which an entity stops existing after or before a year
        if not (past_row and current_row):
            print("! Hmmmm", slug, "does not exist in either the current or past year; skipping")
            continue # skip to the next iteration

        entity = OrderedDict()
        entity['name'] = current_row['name']
        entity['slug'] = current_row['slug']
        for h in data_headers:
            cval = current_row[h]
            pval = past_row[h]
            entity[h] = OrderedDict()
            oh = entity[h]
            oh['current'] = cval
            oh['past'] = pval
            oh['delta'] = None
            oh['delta_rate'] = None

            if cval and pval and cval != 0:
                dx = cval - pval
                oh['delta'] = round(dx, 1) if type(dx) is float else dx
                oh['delta_rate'] = round((100 * dx / cval), 1)
        entities.append(entity)



    # prepare json file to write to
    dest_fname = join(DEST_DATA_DIR, '{0}.json'.format(geoname))
    print("Writing to", dest_fname)
    with open(dest_fname, 'w') as wf:
        obj = OrderedDict()
        obj['meta'] = {'geo': geoname, 'source': 'ACS5',
                'current_year': CURRENT_YEAR, 'past_year': PAST_YEAR}
        obj['entities'] = entities
        json.dump(obj, wf, indent=2)
