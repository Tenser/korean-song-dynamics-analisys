import sys
import numpy as np
import representation

years = [i for i in range(1999, 2021)]
genre_dict = representation.genre_dict


def getGroupRate(data):
    res = []
    for year in years:
        res.append(data[data[:,0] == year, 2].mean(axis=0) * 100)
    return res

def getManRate(data):
    res = []
    for year in years:
        res.append(data[data[:,0] == year, 3].mean(axis=0) * 100)
    return res

def getFeaturingRate(data):
    res = []
    for year in years:
        res.append(data[data[:,0] == year, 4].mean(axis=0) * 100)
    return res

def getGenreRates(data):
    res_dict = {}
    for genre in genre_dict:
        res_dict[genre] = []
        for year in years:
            res_dict[genre].append(data[data[:,0] == year, 5+genre_dict[genre]].mean(axis=0) * 100)
    return res_dict



