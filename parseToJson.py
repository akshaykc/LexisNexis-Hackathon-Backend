'''
Created on Oct 13, 2016

@author: achaluv
'''
import json
import random

dataJson = []
count = 0

with open("addWithLatLong.txt", 'rb') as latLonFile:
    with open("dataJson.txt","wb") as JsonFile:
        for line in latLonFile:
            dataJsonObj = {}
            elems = line.split("\t")
            if len(elems) == 9:
                dataJsonObj['address'] = "|".join(elems[:-2])
                dataJsonObj['latitude'] = elems[7]
                dataJsonObj['longitude'] = elems[8].strip()
                dataJsonObj['revenue'] = random.randrange(0,100)
                dataJsonObj['IQ'] = random.randrange(0,7)
                dataJsonObj['CrossSell'] = random.randrange(0,80)
                dataJsonObj['BV'] = 
                
                dataJson.append(dataJsonObj)
        json.dump(dataJson, JsonFile, sort_keys = True, indent = 4, ensure_ascii=False)