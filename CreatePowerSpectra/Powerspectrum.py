import os
from astropy.io import fits
import subprocess


# Find pca index filename by fmi file content
def findPcaFileName(fmiPath):
    fmi = fits.open(fmiPath)
    fmiContent = open('fmiContent.txt', 'w')
    fmiContent.write(str(repr(fmi[1].header)))
    fmiContent.close()

    fmiContent = open('fmiContent.txt', 'r')
    for line in fmiContent.readlines():
        if line.__contains__("PCA_Index_File"):
            columNumber = int(line.split("field")[1])
            fmiContent.close()
            pcaIndexFilename = str(fmi[1].data).split(", ", 14)[columNumber - 1]
            fmi.close()
            return pcaIndexFilename


# Determines what configurations to accept and gives back time resolution
def acceptMode(modeConfig):
    parts = str(modeConfig).strip().split('_')
    mode = parts[0].strip('\'')

    if mode == "SB":
        if parts[1].strip('\'') in ["31us", "62us", "125us", "250us"] and parts[2].strip('\'') == "0":
            if parts[3].strip('\'') == "249":
                return parts[1].strip('\'')
    elif mode == "E":
        if parts[1].strip('\'') in ["8us", "16us", "31us", "62us", "125us", "250us"] and parts[3].strip('\'') == "0":
            return parts[1].strip('\'')
    elif mode == 'B':
        if parts[1].strip('\'') in ["125us", "250us"]:
            if parts[4].strip('\'') == "249" or parts[4].strip('\'') == "254" or parts[4].strip('\'') == "255":
                return parts[1].strip('\'')
    else:
        return 0


# Indexes all files with correct mode in 1 pca folder and writes them to fileNames.txt
def getMeasurementFilenames(pcaFilePath):
    indexList = []
    fileslist = []
    accepted = 0

    # Parse pca index file data in list
    with fits.open(pcaFilePath) as pcaPath:
        with open('pcaIndex.txt', 'w') as pcaIndex:
            pcaIndex.write(str(repr(pcaPath[1].data)))
    with open('pcaIndex.txt', 'r') as pcaIndex:
        pcaContent = pcaIndex.readlines()

    # Append columnnames with relevant columns from pca index file to list
    columnNames = pcaContent[-1].split("[")[1].split("),")
    for columnName in columnNames:
        if columnName.__contains__("ModeNm"):
            indexList.append(columnNames.index(columnName))  # 4, 7, 10, 13, 16, 19

    # Looks for modes in pca index file and checks whether they are desired. If so it writes them to fileNames.txt
    for row in pcaContent[:-1]:
        colAtIndex = row.split(',')
        if len(colAtIndex) > indexList[0]:
            if colAtIndex[0]:
                for colIdx in indexList:
                    strippedName = str(colAtIndex[colIdx + 1]).strip().strip('\'').split('/')
                    filename = strippedName[1] if strippedName[0] == 'pca' else ''
                    checkname = filename + '.' + str(acceptMode(colAtIndex[colIdx])) + '.' + \
                                colAtIndex[colIdx].split('_')[0].strip().strip('\'')
                    if acceptMode(colAtIndex[colIdx]) not in [0, None] and checkname not in fileslist and checkname:
                        accepted = 1
                        fileslist.append(checkname)
    if accepted:
        return fileslist


def getfilenamestarts(correctfiles):
    starts = []
    for file in correctfiles:
        start = file.strip('\'').split('_')[0]
        if start not in starts:
            starts.append(start)
    return starts


def binningFactor(timeResolution):
    switcher = {
        '250': 1,
        '125': 2,
        '62': 4,
        '31': 8,
        '16': 16,
        '8': 32,
        '4': 64,
        '2': 128,
        '1': 256
    }
    return switcher.get(timeResolution)


# Creates power spectrum using path to observation and gti path
def createPowerSpectrum(datapath, gtipath):
    for file in os.listdir(datapath + '/pca'):
        if file.startswith("@"):
            obsid = str(datapath).split('/')[-1]
            fileparts = file.split('.')
            start = str(fileparts[0].strip('@'))

            timeres = (file.split('.')[2]).split('u')[0]
            binningfactor = str(binningFactor(timeres))
            mode = str(file.split('.')[1])
            subprocess.check_call([
                './WritePowerspectrum.sh',
                datapath + '/pca', file, obsid + '_' + start + '_' + mode + '_' + timeres, binningfactor, gtipath])
            # call fftxte with
            # line 10 binning factor


def getgtipath(objidpath):
    gtipath = ""
    objidparts = objidpath.split('/')[1:]
    for objidpart in objidparts:
        objidpart.strip('\\')
        gtipath += '\/' + objidpart
    return gtipath


def main():
    # directorystructure of main => NS/obsid/pca,fmi,fipc/measfiles
    mainDirectory = "/export/data/jordit/data/BH"
    for objectid in os.listdir(mainDirectory):
        gtipath = getgtipath(mainDirectory + '/' + objectid)

        # If NS or BH are given:
        for obsid in os.listdir(mainDirectory + '/' + objectid):
            if obsid[0].isdigit():
                print("Entering " + obsid)
                if str(obsid)[0].isdigit():
                    pcaFilename = findPcaFileName(mainDirectory + '/' + objectid + '/' + obsid + '/' + "FMI").strip(
                        '\'')
                    pcaFilePath = mainDirectory + '/' + objectid + '/' + obsid + '/' + pcaFilename

                    # Filenames with the right mode
                    correctfiles = getMeasurementFilenames(pcaFilePath)
                    if correctfiles != None:
                        for filename in correctfiles:
                            name = filename.split('.')[0].split('_')[0]
                            timeres = filename.split('.')[1]
                            mode = filename.split('.')[2]
                            shortname = filename.split('.')[0]
                            if not os.path.isfile(mainDirectory + '/' + objectid + '/' + obsid + '/' + 'pca/' + '@' +
                                                  name + '.' + mode + '.' + timeres + '.meta.txt'):
                                open(mainDirectory + '/' + objectid + '/' + obsid + '/' + 'pca/' + '@' + name +
                                     '.' + mode + '.' + timeres + '.meta.txt', 'w').close()
                            with open(mainDirectory + '/' + objectid + '/' + obsid + '/' + 'pca/' + '@' + name +
                                      '.' + mode + '.' + timeres + '.meta.txt', 'a') as metafile:
                                for measfile in os.listdir(mainDirectory + '/' + objectid + '/' + obsid + '/' + 'pca'):
                                    if measfile.startswith(shortname):
                                        metafile.write(measfile + '\n')
                        createPowerSpectrum(mainDirectory + '/' + objectid + '/' + obsid, gtipath)


main()
