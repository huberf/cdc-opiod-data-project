from geopy.geocoders import Nominatim
from time import sleep
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load all data
fileName = "deathsByCountByYear.txt"
dataTable = pd.read_table(fileName)

# Extract all counties
counties = []
rawCounties = dataTable["County"]
filtered = list(set(rawCounties))
print(filtered)
print(len(filtered))

# GPS Pull
geolocator = Nominatim()
name = ""
locations = []
ticker = 0
for i in filtered:
    ticker += 1
    success = False
    while (not success):
        #sleep(1)
        print(ticker)
        try:
            location = geolocator.geocode(i)
            success = True
            try:
                locations += [i, location.latitude, location.longitude]
            except:
                print("Failed!")
        except:
            success = False
print("Spacer: \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print locations
