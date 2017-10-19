import requests as r
from BeautifulSoup import BeautifulSoup
import re
import json

states = json.load(file('statesWithCodes.json'))
years = ['2007']

counties = []
for state in states:
    for year in years:
        print('Gathering data: ', state[0], ' : ' , year)
        data = {
            'survey': 'la',
            'map': 'county',
            'seasonal': 'u',
            'state': state[1],
            'year': year,
            'period': 'M13', # Annual
            'datatype': 'unemployment'
            }

        info = r.post('https://data.bls.gov/map/MapToolServlet', data)
        text = info.text
        soup = BeautifulSoup(text)
        values = soup.findAll('area')
        for i in values:
            raw = i['title']
            vals = raw.split(', ')
            countyName = vals[0][9:]
            unemploymentRate = vals[1][20:]
            cleaned = {
                    'county': countyName,
                    'unemploymentRate': unemploymentRate,
                    'state': state[0],
                    'year': year
                    }
            counties += [cleaned]

print(counties)
stringData = json.dumps(counties)
outputFile = file('unemploymentByCounty.json', 'w')
outputFile.write(stringData)
