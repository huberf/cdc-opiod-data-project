from scipy import stats
import numpy as np
import json

# Load data into the x and y
unemploymentFileName = '../unemploymentByCounty.json'
unemploymentFile = json.load(file(unemploymentFileName))

deathFileName = '../DeathsByCountyUnsuppressed2010-2015.json'
deathFile = json.load(file(deathFileName))

# x is arbitrarily death count and y is unemployment
x = []
y = []
noMatchCount = 0
matchCount = 0
# The death data file has county names mapped to values so we can do the below
for i in unemploymentFile:
    try:
        deaths = deathFile[i['county']]
        x += [deaths]
        y += [i['unemploymentRate']]
        matchCount += 1
    except:
        noMatchCount += 1


print('--------- X ----------')
print(x)
print('--------- Y ----------')
print(y)

# Convert lists to Numpy arrays

x_array = np.array(x).astype(np.float)
y_array = np.array(y).astype(np.float)

slope, intercept, r_value, p_value, std_err = stats.linregress(x_array, y_array)

# Show meta process info
print('Match count: ', matchCount)
print('No match count: ', noMatchCount)
print()

# Show general stats
print('Slope: ', slope)
print('Intercept: ', intercept)
print('r-value: ', r_value)
print('p-value: ', p_value)
print('Standard error: ', std_err)

# Show how well the model works
print('r-squared: ', r_value**2)
