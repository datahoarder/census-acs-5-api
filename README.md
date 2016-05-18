

Sample call to get total population for the entire U.S., ACS5 2014:

http://api.census.gov/data/2014/acs5?key=YOUR_KEY&for=us:*&get=B01003_001E


Sample call to get a bunch of interesting attributes for every U.S. state -- the important key-value pair is: `for=state:*`:


http://api.census.gov/data/2014/acs5?key=YOUR_KEY&for=state:*&get=B01003_001E,B11011_001E,B11011_002E,B11011_003E,B01001_002E,B01001_026E,B01002_001E,B23006_001E,B03002_002E,B03003_003E,B03002_003E,B03002_004E,B03002_005E,B03002_006E,B03002_007E,B03002_008E,B03002_009E,B23006_023E,B07001_017E,B07001_081E,B05002_004E,B05001_006E,B06011_001E,B06012_004E


