from scipy import stats
from scipy.stats.stats import pearsonr
import numpy as np
import json
import matplotlib.pyplot as plt

# Load unemployment data (local and national)
unemploymentFileName = '../unemploymentByCounty.json'
unemploymentFile = json.load(open(unemploymentFileName))
nationalUnemployment = json.loads(open('../unemploymentNationalByYear.json').read())

# deathFileName = '../DeathsByCountyUnsuppressed2010-2015.json'
# deathFile = json.load(open(deathFileName))

# Load opioid death data by year for all years included below
deathData = {}
years = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
for i in years:
    data = json.load(open('../opioid_deaths/' + i + '.json'))
    deathData.update({i: data})

# Retreives the death per 1000000 by count name and year
def getDeathCountByCounty(countyName, year):
    deathFile = deathData[year]
    deathSpecifics = deathFile[countyName]
    deathCount = deathSpecifics['Death']
    population = deathSpecifics['Population']
    hundredThousand = 100000.0
    deathPerPop = (deathCount) * (hundredThousand/population)
    return deathPerPop

# County data graph stores values for each county over the data lifetime
countyDataGraph = {}
# Shows how many counties could be mapped to data
noMatchCount = 0
matchCount = 0
# The death data file has county names mapped to values so we can do the below
for i in unemploymentFile:
    try:
        countyName = i['county']
        deaths = getDeathCountByCounty(countyName, i['year'])
        # Check if the data graph for the county name already been initialized
        try:
            countyDataGraph[countyName]
        except:
            countyDataGraph.update({countyName: []})
        # Clean unemployment by comparing to national average
        cleanedUnemployment = float(i['unemploymentRate']) - nationalUnemployment[i['year']]
        #cleanedUnemployment = i['unemploymentRate']
        newData = [cleanedUnemployment, deaths]
        # Add the data to the county data
        countyDataGraph[countyName] += [newData]
        matchCount += 1
    except:
        # As there isn't opioid data for every county this is called
        noMatchCount += 1

# Show meta process info
print('Match count: ', matchCount)
print('No match count: ', noMatchCount)
print()

average_r_2_value = 0.0
count = 0.0
maxRSquared = 0
r_2_values = {}
# Tracking of positive and negative correlation
slopeCount = {'up': 0, 'down': 0}
# Map of all slope values by county code
slope_values = {}
countyNameToCode = json.load(open('../CountyNameToCode.json'))
# Convert lists to Numpy arrays
index = 0
# Long term collection of x and y values to be showed at the end
x_acc = []
y_acc = []

for key, value in list(countyDataGraph.items()):
    # Setup values to be viewed by the x and y
    # X is unemployment and Y is death rate
    x = []
    y = []
    for i in value:
        # Scrub for zero values
        if i[1] != 0 and i[0] != 0:
            x += [i[0]]
            y += [i[1]]

    if (len(x) == 0):
        continue

    # Show values in testing
    print('--------- X ----------')
    print(x)
    print('--------- Y ----------')
    print(y)
    x_array = np.array(x).astype(np.float)
    y_array = np.array(y).astype(np.float)

    # Generate linear regression values for data
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_array, y_array)

    # Show the county name
    print(key)
    # Add the raw values normalized by division of the the slope
    # limited to relations by states for which uenmployment is a factor
    # Supports filtering by the two character state abbreviation
    if (key[-2:] != "Random" and r_value**2 > 0.05):
        #x_acc += [np.average(x_array)]
        #y_acc += [slope]
        #
        #x_acc += x_array.tolist()
        #y_acc += np.divide(y_array, 1).tolist()
        #
        # For graphing display values divided by the slope
        # to normalize
        x_acc += np.divide(x_array, slope).tolist()
        y_acc += np.divide(y_array, slope).tolist()

    index += 1
    '''
    if index == -1:
        print(x_array)
        print(y_array)
        plt.plot(x_array, y_array, "ro")
        plt.xlabel("Unemployment")
        plt.ylabel("Death Per 100000")
        plt.show()
    '''

    # Log whether the slope was positive or negative for this county
    if slope > 0:
        slopeCount['up'] += 1
    else:
        slopeCount['down'] += 1

    # LEGACY: Detection of highest r^2 value
    if (r_value**2 > maxRSquared):
        print(key)
        print(r_value**2)
        maxRSquared = r_value**2

    # Save useful data such as r^2 and slope values
    countyCode = countyNameToCode[key]
    r_2_values.update({countyCode: r_value**2})
    slope_values.update({countyCode: slope})

    minimumCorrelation = 0.05
    # Compute data set wide values limited by county
    # classifications
    if (r_value**2 > minimumCorrelation):
        currentRSum = average_r_2_value * count
        count += 1.0
        currentRSum += r_value**2
        average_r_2_value = currentRSum/count

    # Show general stats
    print('Slope: ', slope)
    print('Intercept: ', intercept)
    print('r-value: ', r_value)
    print('p-value: ', p_value)
    print('Standard error: ', std_err)

    # Show how well the model works for the specific county
    print('r-squared: ', r_value**2)

# Write data to files
r2Counties = open('r_2_values.json', 'w')
r2Counties.write(json.dumps(r_2_values))
slopeCounties = open('slope_values.json', 'w')
slopeCounties.write(json.dumps(slope_values))

print('--------------------------------')
print('Average r-squared: ', average_r_2_value)
print('Using ' + str(count) + ' out of ' + str(index))
print('Data set wide slope correlation: ')
print(slopeCount)

# Plot data set wide values tracked
plt.plot(x_acc, y_acc, "ro", ms = "0.5")
plt.xlabel("Unemployment vs. National Average / Slope")
plt.ylabel("Death Per 100000 / Slope")
plt.show()

