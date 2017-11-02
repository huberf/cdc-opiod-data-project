# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
import json

# Read Data as county code (fips) to dataValue (int)
jsonFile = open(sys.argv[1], "r")
countyToData = json.load(jsonFile)
jsonFile.close()

# Load the SVG map
svg = open('counties.svg', 'r').read()


# Load into Beautiful Soup
soup = BeautifulSoup(svg, "xml")

# Find counties
paths = soup.findAll('path')

# Map colors
colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

# County style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'


# Color the counties based on unemployment rate
#print(countyToDeathsMap)
for p in paths:
     
    if p['id'] not in ["State_Lines", "separator"]:
        # pass
        try:
            rate = countyToData[p['id']]
        except:
            continue
             
        if rate > 0.6:
            color_class = 5
        elif rate > 0.4:
            color_class = 4
        elif rate > 0.2:
            color_class = 3
        elif rate > 0.1:
            color_class = 2
        elif rate > 0.05:
            color_class = 1
        else:
            color_class = 0
 
        color = colors[color_class]
        p['style'] = path_style + color

# Output map
print(soup.prettify())

#crudeDeaths = list(filter(lambda x: x!=-1, list(countyToData.values())))
#fq = np.median(list(filter(lambda x: x<np.median(crudeDeaths), crudeDeaths)))
#tq = np.median(list(filter(lambda x: x>np.median(crudeDeaths), crudeDeaths)))
#print(np.min(crudeDeaths), fq, np.median(crudeDeaths), tq, np.max(crudeDeaths))
