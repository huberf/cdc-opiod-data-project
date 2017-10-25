from scipy import stats
import numpy as np
import json

# Load data into the x and y
unemploymentFileName = '../unemploymentByCounty.json'
unemploymentFile = json.load(open(unemploymentFileName))

deathFileName = '../DeathsByCountyUnsuppressed2010-2015.json'
deathFile = json.load(open(deathFileName))

# TODO: Integrate data source which allows death data selection by year
def getDeathCountByCounty(countyName, year):
    return deathFile[countyName]

# County data graph stores values for each county over the data lifetime
countyDataGraph = {}
noMatchCount = 0
matchCount = 0
# The death data file has county names mapped to values so we can do the below
for i in unemploymentFile:
    try:
        countyName = i['county']
        deaths = getDeathCountByCounty(countyName, i['year'])
        try:
            countyDataGraph[countyName]
        except:
            countyDataGraph.update({countyName: []})
        newData = [i['unemploymentRate'], deaths]
        countyDataGraph[countyName] += [newData]
        matchCount += 1
    except:
        noMatchCount += 1

# Show meta process info
print('Match count: ', matchCount)
print('No match count: ', noMatchCount)
print()

average_r_2_value = 0.0
count = 0.0
# Convert lists to Numpy arrays
for key, value in countyDataGraph.iteritems():
    x = []
    y = []
    for i in value:
        x += [i[0]]
        y += [i[1]]
    print('--------- X ----------')
    print(x)
    print('--------- Y ----------')
    print(y)
    x_array = np.array(x).astype(np.float)
    y_array = np.array(y).astype(np.float)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x_array, y_array)

    currentRSum = average_r_2_value * count
    count += 1.0
    currentRSum += r_value
    average_r_value = currentRSum/count

    # Show general stats
    print('Slope: ', slope)
    print('Intercept: ', intercept)
    print('r-value: ', r_value)
    print('p-value: ', p_value)
    print('Standard error: ', std_err)

    # Show how well the model works
    print('r-squared: ', r_value**2)

print('--------------------------------')
print('Average r-squared: ', average_r_2_value)
