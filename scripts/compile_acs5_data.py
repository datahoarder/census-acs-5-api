from collections import defaultdict, OrderedDict
from os.path import join
from os import makedirs
from glob import glob
import csv
import re
import json

FETCHED_DATA_DIR = join('data', 'fetched')
WRANGLED_DATA_DIR = join('data', 'wrangled')
DEST_FILENAME =  join(WRANGLED_DATA_DIR, 'acs5-compiled.csv')
GEO_NAME_HEADERS = [
    ('us', ['us']),
    ('state', ['state']),
    ('congressional+district', ['state', 'congressional district']),
    ('county', ['state', 'county']),
    ('zip+code+tabulation+area', ['zip code tabulation area']),
]

VAR_NAMES_TO_SLUGS = OrderedDict()
with open(join('data', 'acs5-var-lookups.csv')) as rf:
    dlist = list(csv.DictReader(rf))
    # return a list of dicts, e.g.
    # [
    #    {"B01003_001E": "total_population"},
    #    {"B11011_001E": "total_households"},
    # ]
    for r in dlist:
        VAR_NAMES_TO_SLUGS[r['name']] = r['slug']

COMPILED_HEADERS = ['name', 'geo', 'slug', 'year'] + list(VAR_NAMES_TO_SLUGS.values())


# prepare the csv
dest_file = open(DEST_FILENAME, 'w')
dest_csv = csv.DictWriter(dest_file, fieldnames=COMPILED_HEADERS)
dest_csv.writeheader()

# let's get all the fetched files together
for geoname, geoname_columns in GEO_NAME_HEADERS:
    src_dir = join(FETCHED_DATA_DIR, geoname)
    for src_fn in glob(join(src_dir, '*.json')):
        # get the year
        print(src_fn)
        with open(src_fn, 'r') as rf:
            data = json.load(rf)
        year = re.search(r'20\d\d', src_fn).group()
        # convert each variable name in the header to a readable slug
        headers = [VAR_NAMES_TO_SLUGS.get(col, col) for col in data[0]]
        # remaining rows are datarows
        datarows = [dict(zip(headers, row)) for row in data[1:]]


        for row in datarows:
            entity = {}
            entity['name'] = row['NAME']
            entity['geo'] =  geoname
            entity['slug'] = '-'.join([row[c] for c in geoname_columns])
            entity['year'] = year

            for varslug in VAR_NAMES_TO_SLUGS.values():
                entity[varslug] = row[varslug]

            dest_csv.writerow(entity)


dest_file.close()
