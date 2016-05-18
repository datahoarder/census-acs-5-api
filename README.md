# Fun with the Census API for American Community Survey (5-year) data

This repo shows how to programmatically fetch data from the [Census API](http://www.census.gov/data/developers/data-sets.html). Specifically, the ACS-5-year dataset, which is documented here:

http://www.census.gov/data/developers/data-sets/acs-survey-5-year-data.html


## What this repo's code fetches

The code in this repo, specifically [scripts/fetch_acs5_data.py](scripts/fetch_acs5_data.py) pulls several dimensions of data:

- For every year from 2009 to 2014
  - For every state, county, congressional district, and zip code (plus, the U.S. at large)
    - Extract 25 interesting data points ([see my lookup table](data/acs5-var-lookups.csv))

## How to test out the API via browser

You can find a long list of sample calls here:

[http://api.census.gov/data/2014/acs5/examples.html](http://api.census.gov/data/2014/acs5/examples.html)

You should sign up for a key here: [http://api.census.gov/data/key_signup.html](http://api.census.gov/data/key_signup.html)

But in the meantime, these sample calls should work:

##### Get total population for the U.S. in the 2014 ACS-5-year data

http://api.census.gov/data/2014/acs5?key=YOUR_KEY&for=us:*&get=B01003_001E


##### Get several data points for every state in the 2014 ACS-5-year data


Sample call to get a bunch of interesting attributes for every U.S. state -- the important key-value pair is: `for=state:*`:


http://api.census.gov/data/2014/acs5?key=YOUR_KEY&for=state:*&get=B01003_001E,B11011_001E,B11011_002E,B11011_003E,B01001_002E,B01001_026E,B01002_001E,B23006_001E,B03002_002E,B03003_003E,B03002_003E,B03002_004E,B03002_005E,B03002_006E,B03002_007E,B03002_008E,B03002_009E,B23006_023E,B07001_017E,B07001_081E,B05002_004E,B05001_006E,B06011_001E,B06012_004E



# How to use this code

The Python in this repository has been tested on __Python 3.5__

This repo contains all the finished data...you don't have to run any of the scripts yourself to get the data that I've fetched and wrangled (check out the [data/](data/) folder yourself).

But if you want to run this code, clear out the [data/fetched/](data/fetched/) directory. Then run these Python scripts in sequence:

~~~sh
$ python scripts/fetch_acs5_data.py 
# creates data/fetched folders and data files
$ python scripts/compile_acs5_data.py
# creates data/compiled/acs5-compiled.csv, 
# a flat file of all the fetched data 
$ python scripts/compile_acs5_percentages.py 
# reads from  from acs5-compiled.csv
#  and creates data/compiled/acs5-compiled-percentages.csv
$ python scripts/wrangle_acs5_deltas.py 
# reads from data/compiled/acs5-compiled-percentages.csv
#  and creates data/wrangled/acs-delta-{year1}-{year2}/{geoname}.json
#  which is a relatively easy-to-use file that any app can deserialize
~~~


The most complex scripts involve the compilation and wrangling phase. In the end, the 


Sample call to get total population for the entire U.S., ACS5 2014:

