#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 19:54:38 2017

The data extraction module takes in a file path to a 

@author: Safin
"""

import sys
import pandas as pd
from geopy import Nominatim
import json

"""Extracts county code given the county name"""
def getCountyCode(countyName):
    nameToCodeJson = open("CountyNameToCode.json", "r")
    countyNameToCode = json.load(nameToCodeJson)
    return(str(countyNameToCode[countyName]))

""" Encapsulates data into a mapping from county to the relevant data about it. The filePath must link to a file that
can be read by panda. RelevantStatistics must be in the form of a list with elements being columns of the data table.
Data is stored in a panda dataframe"""
def extractCountyDataAsDataFrame(filePath, relevantStatistics = ["Deaths"], countyStatisticMap = {}):
    myData = pd.read_table(filePath)
    countyGroup = myData["County"].dropna()
    countyStatisticMap = {}
    
    for county in countyGroup.as_matrix().tolist():
        statsToAdd = myData[myData.County == county][relevantStatistics]
        if not county in countyStatisticMap:
            countyStatisticMap[county] = statsToAdd
        else:
            countyStatisticMap[county] = pd.concat(countyStatisticMap[county], statsToAdd)
    
    return countyStatisticMap

""" Same as extractCountyDataAsDataFrame except the data is stored as a list of lists rather than a dataframe"""
def extractCountyDataAsList(filePath, relevantStatistics = ["Deaths"], countyStatisticMap = {}):
    myData = pd.read_table(filePath)
    relevantData = myData[["County"] + relevantStatistics]
    
    for infoList in relevantData.as_matrix().tolist():
        key = infoList[0]
        if not key in countyStatisticMap:
            countyStatisticMap[key] = [infoList[1::]]
        else:
            countyStatisticMap[key] = countyStatisticMap[key]+[infoList[1::]]
    del countyStatisticMap["nan"]
    return countyStatisticMap

""" Filters out keys and values from a dictionary"""
def filterDictionary(dictionary, keyFilter = lambda x: True, valueFilter = lambda x: True):
    filteredDictionary = {}
    for k, v in dictionary.items():
        if (valueFilter(v) and keyFilter(k)):
            filteredDictionary[k] = v
    return filteredDictionary

""" Maps functions onto keys or values of a dictionary"""
def mapDictionary(dictionary, keyMap = (lambda x: x), valueMap = (lambda x: x)):
    mappedDictionary = {}
    for k, v in dictionary.items():
        mappedDictionary[keyMap(k)] = valueMap(v)
    return mappedDictionary

"""Returns the gpsCoordinates for a place as a tuple of latitude and longitude"""
def gpsCoordinates(placeName):
    geolocator = Nominatim()
    location = geolocator.geocode(placeName)
    return (location.latitude, location.longitude)

"""Convert to json"""
def writeToJSON(fileName, dictionary):
    jsonFileToWrite = open(fileName + ".json", 'w')
    json.dump(dictionary, jsonFileToWrite)
    jsonFileToWrite.close()

def getDeathsPerTenThousand(df):
    deaths = df["Deaths"].as_matrix()[0]
    population = df["Population"].as_matrix()[0]
    if deaths == "Suppressed":
        return -1
    else:
        deaths = float(deaths)
        population = float(population)
        return 10**5 * 1.0 *deaths/population

if (len(sys.argv)==2):
    fileName = sys.argv[1]
    countyToStatistics = extractCountyDataAsDataFrame(fileName, relevantStatistics=["Deaths", "Population"])
    countyCodeToCrudeRate = mapDictionary(countyToStatistics, keyMap=getCountyCode, valueMap=getDeathsPerTenThousand)
    
    jsonFileName = fileName.split(".")[0] + "CrudeRate"
    writeToJSON(jsonFileName, countyCodeToCrudeRate)
    