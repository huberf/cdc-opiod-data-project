# Opioid Epidemic Relief Project

## Datasets
* `opioid_deaths/*.json` - Opioid mortality raw value count by county for every
  year from 1999 to 2015
* `unemploymentByCounty.json` - Includes unemployment data for every county from
  1999 to 2016
* `Part_D_Opioid_Prescribing_Change_Geographic_2013_2014_backup.csv` - Includes
  opioid prescription rates from 2013-2014 by county.

## Helper Tools
* boilerplateDataLoad.py - Automatically loads the main data set and can be
  copied and edited to do complex data analysis.

## Analysis
Under the `/analyis` subdirectory are python scripts to perform statistical
operations on the data above. Currently the system supports correlating opioid
deaths with unemployment data.

## Replication
Want to gain the same insights and follow our process. Do the below.
1. Enter the `analysis/` directory.
2. Run `python3 deathsAndUnemploymentRegression.py`. A graph should pop up and
   statistics should be printed to terminal. In the background two files
   containing the slope and r^2 values will have been written to the disk.
3. To visualize this data you can employ `dataVisualization.py` and the
   accompanying `counties.svg`. To write the r^2 values run `python3
   dataVisualization.py r_2_values.json > r2byCounty.svg` and load the SVG
   inside a web browser.
4. Using the above, you can write any data that is mapped to by the county code.
5. To recreate our analysis of prescription rates, run `python3
   prescriptionAndDeathsRegression.py` and you can analyze the output graphs and
   printed statistics. You can also view the slope and r^2 values in files
   generated in the same directory.
6. To recreate the analysis of the link between unemployment and prescription,
   run `python3 unemploymentAndPrescriptionRegression.py` and you can then
   review the output graphic showing the raw unemployment and prescription
   data points in a point cloud and also analyze the county by county link via
   manipulation and viewing of `unemployment_prescription_values.json` (slope) or its
   companion r^2 file.

### Replication of Data Retreival
1. In the main directory simply run `python unemploymentCrawler.py` and wait for
   the process to complete (will likely take several hours). It will write all
   the data to `unemploymentByCounty.json`.
2. For the BLS website, you will have to manually retreive entry as automated
   scripting of confirming use of the site is against policy.
