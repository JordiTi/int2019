import os
import numpy as np
from numpy import array
import random


def loaddata(nspath, bhpath):

    topdict = {"BH": [], "NS": []}
    datadict = {}

    print("Reading files...")

    for objectid in os.listdir(nspath):
        objectpath = nspath + objectid + '/'
        datalist = []
        for file in os.listdir(objectpath):
            with open(objectpath + file, 'r') as nsFile:
                nsData = nsFile.read().splitlines()
                observationdata = []
                for line in nsData:
                    line = line.strip()
                    observationdata.append(float(line))
            datalist.append([str(file).split('_')[0], observationdata])
        datadict[str(objectid)] = datalist
    topdict["NS"] = datadict
    datadict = {}

    for objectid in os.listdir(bhpath):
        objectpath = bhpath + objectid + '/'
        datalist = []
        for file in os.listdir(objectpath):
            with open(objectpath + file, 'r') as bhFile:
                bhData = bhFile.read().splitlines()
                observationdata = []
                for line in bhData:
                    line = line.strip()
                    observationdata.append(float(line))
            datalist.append([str(file).split('_')[0], observationdata])
        datadict[str(objectid)] = datalist

    topdict["BH"] = datadict

    print("Done reading")

    return topdict


def gettraindata(datadict, target):

    bhdata = []
    nsdata = []
    for object in datadict["BH"]:
        if object != target:
            for data in datadict["BH"][object]:
                bhdata.append(data[1])
    bhlabels = [1] * len(bhdata)
    i = 0
    while i < len(bhdata):
        randomobj = random.choice(list(datadict["NS"].keys()))
        randomdata = random.choice((datadict["NS"][randomobj]))
        if randomobj != target and randomdata[1] not in nsdata:
            nsdata.append(randomdata[1])
            i = i + 1
    nslabels = [0] * len(nsdata)
    train_data = np.append(bhdata, nsdata)
    train_labels = bhlabels + nslabels
    train_data = train_data.reshape(len(bhdata * 2), -1)
    train_labels = array(train_labels)
    return train_data, train_labels

