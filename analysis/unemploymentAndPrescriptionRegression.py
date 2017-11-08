# Years covered by data 2013-2014
from scipy import stats
import numpy as np
import csv
import json
import matplotlib.pyplot as plt

print('Loading data...')
# Load and format prescription data
prescriptionDataFile = open('../Part_D_Opioid_Prescribing_Change_Geographic_2013_2014_backup.csv', encoding="ISO-8859-1")
contents = csv.reader(prescriptionDataFile, dialect='excel')
prescriptionData = []
for i in contents:
    prescriptionData += [i]

prescriptionByCounty = []
# Loop over data except for header rows
for i in prescriptionData[1:]:
    countyName = i[3] + ' County, ' + i[1]
    values2013 = i[8]
    values2014 = i[12]
    prescriptionByCounty += [{
        'county': countyName,
        '2013': values2013,
        '2014': values2014
    }]

#print(prescriptionByCounty)


'''
deathData = {}
years = ['2013', '2014']
for i in years:
    data = json.load(open('../opioid_deaths/' + i + '.json'))
    deathData.update({i: data})
'''
# Load unemployment data (local and national)
unemploymentFileName = '../unemploymentByCounty.json'
unemploymentFile = json.load(open(unemploymentFileName))
nationalUnemployment = json.loads(open('../unemploymentNationalByYear.json').read())

##############
# Processing #
##############
def getUnemploymentByCounty(countyName, year):
    try:
        for i in unemploymentFile:
            #thisCounty = i['county'][0:-4] + ' County' + i['county'][-4:]
            thisCounty = i['county']
            if thisCounty == countyName and i['year'] == year:
                return i['unemploymentRate']
    except:
        print('Something went wrong during unemployment retreival.')

# County data graph stores values for each county over the data lifetime
countyDataGraph = {}
noMatchCount = 0
matchCount = 0
print('Gathering and matching all the data. This may take a while.')
for i in prescriptionByCounty:
    try:
        countyName = i['county']
        # Collect unemployment data
        unemployment2013 = getUnemploymentByCounty(countyName, '2013')
        unemployment2014 = getUnemploymentByCounty(countyName, '2014')
        try:
            countyDataGraph[countyName]
        except:
            countyDataGraph.update({countyName: []})
        newData = [
                [unemployment2013, i['2013']],
                [unemployment2014, i['2014']]
                ]
        countyDataGraph[countyName] += newData
        matchCount += 1
    except:
        noMatchCount += 1

# Show meta process info
print('Match count: ', matchCount)
print('No match count: ', noMatchCount)
print()

# Compute statistics about collected and formatted data

average_r_2_value = 0.0
count = 0.0
maxRSquared = 0
r_2_values = {}
slopeCount = {'up': 0, 'down': 0}
slope_values = {}
countyNameToCode = json.load(open('../CountyNameToCode.json'))
# Convert lists to Numpy arrays
index = 0
x_acc = []
y_acc = []

for key, value in list(countyDataGraph.items()):
    x = []
    y = []
    # Add values and skip entry if either are undefined
    for i in value:
        if i[0] != '' and i[1] != '':
            x += [i[0]]
            y += [i[1]]
        else:
            continue

    if (len(x) == 0):
        continue
    print('--------- X ----------')
    print(x)
    print('--------- Y ----------')
    print(y)
    try:
        x_array = np.array(x).astype(np.float)
        y_array = np.array(y).astype(np.float)
    except:
        continue

    slope, intercept, r_value, p_value, std_err = stats.linregress(x_array, y_array)

    print(key)
    if (key[-2:] != "Random"):
        '''
        if (len(y_array) == 2):
            x_acc += [x_array[1] - x_array[0]]
            print(x_acc)
            y_acc += [slope]
        '''
        # Uncomment code to show piecewise values
        x_acc += x_array.tolist()
        y_acc += y_array.tolist()
        #y_acc += np.divide(y_array, 1).tolist()

    index += 1

    if slope > 0:
        slopeCount['up'] += 1
    else:
        slopeCount['down'] += 1

    if (r_value**2 > maxRSquared):
        print(key)
        print(r_value**2)
        maxRSquared = r_value**2

    # Save useful data
    try:
        countyCode = countyNameToCode[key]
        r_2_values.update({countyCode: r_value**2})
        slope_values.update({countyCode: slope})
    except:
        print('Unable to map to a known county code')

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
r2Counties = open('unemployment_prescription_r_2_values.json', 'w')
r2Counties.write(json.dumps(r_2_values))
slopeCounties = open('unemployment_prescription_values.json', 'w')
slopeCounties.write(json.dumps(slope_values))

print('--------------------------------')
print('Average r-squared: ', average_r_2_value)
print(slopeCount)

# Perform linear regression on all accumulated unemployment and prescription data
# independent of county
cleaned_x = []
cleaned_y = []
for i in range(len(x_acc)):
    if not np.isnan(x_acc[i]):
        cleaned_x += [x_acc[i]]
        cleaned_y += [y_acc[i]]
    else:
        print(x_acc[i])
        print('Not clean')
x_array = np.array(cleaned_x).astype(np.float)
y_array = np.array(cleaned_y).astype(np.float)
print(x_array)
print('---------------')
print(y_array)
slope, intercept, r_value, p_value, std_err = stats.linregress(x_array, y_array)
print('--------------------------------')
print('Data set wide slope: ', slope)
print('Data set wide r^2: ', r_value**2)
print()

print('Showing plot.')
plt.plot(x_acc, y_acc, "ro", ms = "0.5")
plt.xlabel("Unemployment")
plt.ylabel("Prescription")
plt.show()

