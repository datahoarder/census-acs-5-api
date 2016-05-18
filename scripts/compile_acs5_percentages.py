from os.path import join
import csv

DATA_DIR = 'data'
COMPILED_DIR = join(DATA_DIR, 'compiled')
SRC_FILENAME =  join(COMPILED_DIR, 'acs5-compiled.csv')
DEST_FILENAME = join(COMPILED_DIR, 'acs5-compiled-percentages.csv')

KEEPER_HEADERS = ['name', 'geo', 'slug', 'year',
                  'median_age', 'median_per_capita_income', 'median_household_income']
STAT_HEADERS = {
    'total_households': ['family_households', 'married_households'],
    'total_population': ['males', 'females', 'adults_25_to_64',
                         'not_hispanic_or_latino', 'hispanic_or_latino',
                         'white', 'black', 'american_indian', 'asian',
                         'pacific_islander', 'other_race', 'mixed_race',
                         'lived_in_same_house', 'moved_from_abroad',
                         'not_us_citizen', 'born_in_other_state',
                         'below_poverty_level'
                        ],
    'adults_25_to_64': ['adults_25_to_64_with_bachelor_degrees_plus'],
}
CUSTOM_HEADERS = ['non_white_pct']
TOTALS_HEADERS = list(STAT_HEADERS.keys())
PCT_HEADERS = []
for column_list in STAT_HEADERS.values():
    for colname in column_list:
        PCT_HEADERS.append(colname + '_pct')


ALL_HEADERS = KEEPER_HEADERS + TOTALS_HEADERS + PCT_HEADERS + CUSTOM_HEADERS

# prepare destination file
print("Writing to", DEST_FILENAME)
dest_file = open(DEST_FILENAME, 'w')
dest_csv = csv.DictWriter(dest_file, fieldnames=ALL_HEADERS)
dest_csv.writeheader()


# open the source data
with open(SRC_FILENAME, 'r') as rf:
    print("Extracting from", SRC_FILENAME)
    datarows = list(csv.DictReader(rf))

for row in datarows:
    d = {}
    for k in KEEPER_HEADERS + TOTALS_HEADERS:
        d[k] = row[k]
    # now to calculate each ratio
    for total_key, pct_keys in STAT_HEADERS.items():
        total_val = int(row[total_key])
        for pkey in pct_keys:
            pval = row[pkey]
            if total_val == 0 or pval == '':
                d[pkey + '_pct'] = None
            else:
                d[pkey + '_pct'] = round(100 * int(pval) / total_val, 1)
    # finally, do some custom tallying
    d['non_white_pct'] = round(100 - d['white_pct'], 1) if d['white_pct'] else 100
    dest_csv.writerow(d)


dest_file.close()
