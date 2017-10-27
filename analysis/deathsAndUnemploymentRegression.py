from scipy import stats
import numpy as np
import json

# Load data into the x and y
unemploymentFileName = '../unemploymentByCounty.json'
unemploymentFile = json.load(open(unemploymentFileName))

# deathFileName = '../DeathsByCountyUnsuppressed2010-2015.json'
# deathFile = json.load(open(deathFileName))
deathData = {}
years = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
for i in years:
    data = json.load(open('../opioid_deaths/' + i + '.json'))
    deathData.update({i: data})

# TODO: Integrate data source which allows death data selection by year
def getDeathCountByCounty(countyName, year):
    deathFile = deathData[year]
    deathSpecifics = deathFile[countyName]
    deathCount = deathSpecifics['Death']
    population = deathSpecifics['Population']
    deathPercent = (deathCount * 100000.0)/population
    print(deathPercent)
    return deathPercent

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
maxRSquared = 0
r_2_values = {}
slopeCount = [0, 0]
slope_values = {}
countyNameToCode = json.load(open('../CountyNameToCode.json'))
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

    if slope > 0:
        slopeCount[0] += 1
    else:
        slopeCount[1] += 1

    if (r_value**2 > maxRSquared):
        print(key)
        print(r_value**2)
        maxRSquared = r_value**2

    # Save useful data
    countyCode = countyNameToCode[key]
    r_2_values.update({countyCode: r_value**2})
    slope_values.update({countyCode: slope})

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

    # Show how well the model works
    print('r-squared: ', r_value**2)

# Write data to files
r2Counties = open('r_2_values.json', 'w')
r2Counties.write(json.dumps(r_2_values))
slopeCounties = open('slope_values.json', 'w')
slopeCounties.write(json.dumps(slope_values))

print('--------------------------------')
print('Average r-squared: ', average_r_2_value)
print(slopeCount)
