# Opioid Epidemic Relief Project

## Datasets
* [Underlying Cause of Death, 1999-2015.txt](https://github.com/huberf/cdc-opiod-data-project/blob/master/Underlying%20Cause%20of%20Death%2C%201999-2015.txt) - Contains >4000 entries from 1999 to
  2015 grouped by factors such as year, weekday, gender, etc.
* Opiod Deaths by County 1999-2015.txt - Includes 52,860 rows of data grouped
  by census region, county and year.
* unemploymentByCounty.json - Includes unemployment data for every county from
  1999 to 2016

## Helper Tools
* boilerplateDataLoad.py - Automatically loads the main data set and can be
  copied and edited to do complex data analysis.

## Analysis
Under the `/analyis` subdirectory are python scripts to perform statistical
operations on the data above. Currently the system supports correlating opioid
deaths with unemployment data.
