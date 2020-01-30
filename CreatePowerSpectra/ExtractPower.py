import os

# Strips power from powerspectrum file and saves it in a text file

basePathname = '/net/Virgo01/data/users/timmermans/reb+100/BH/'
for directory in os.listdir(basePathname):
    objectpath = basePathname + directory + '/'
    for obsid in os.listdir(objectpath):
        measurementpath = objectpath + obsid
        with open(measurementpath, 'r') as file:
            with open(objectpath + obsid.split('.txt')[0] + '_reb.txt', 'a') as powerFile:
                    data = file.readlines()
                    for line in data:
                        line = line.strip()
                        if line[0].isdigit():
                            num = float(line.split()[1])
                            powerFile.write(str(num)+'\n')

        os.remove(measurementpath)

