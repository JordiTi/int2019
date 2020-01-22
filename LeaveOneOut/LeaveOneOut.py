# From the path to the neutron star powerspectra and the path to the
# black hole power spectra (powers only with a power on each new line)
# Train either a neural network, logistic regression or random forest classifier


import Data as dt
import numpy as np
import Plotting
from numpy import array
import sys
import Training as tr

# Get flags
learntype = str(sys.argv[1])
rebinning = str(sys.argv[2])
nodes = str(sys.argv[3])

# Write a list of all objects
nsPath = ''
bhPath = ''
targetdir = ''
colorpath = ''

# Dictionary in dictionary
datadict = dt.loaddata(nsPath, bhPath)

for objecttype in datadict.keys():
    for objectid in datadict[objecttype]:


        # Get the data
        testlist = datadict[objecttype][objectid]
        test_data = [objdatapair[1] for objdatapair in testlist]
        test_obs = [objdatapair[0] for objdatapair in testlist]
        label = 1 if objecttype == "BH" else 0
        test_labels = [label] * len(test_data)
        train_data, train_labels = dt.gettraindata(datadict, objectid)

        s = np.arange(train_labels.shape[0])
        np.random.shuffle(s)
        train_data = train_data[s]
        train_labels = train_labels[s]

        train_labels = array(train_labels)
        test_labels = array(test_labels)
        print("\nTesting: " + objectid + '\n')
        accuracylist = []

        if (sys.argv[1]) == "RF":
            accuracylist = tr.trainRF(train_data, test_data, train_labels, test_labels, objectid, label, rebinning)
        if (sys.argv[1]) == "NN":
            accuracylist = tr.trainNN(train_data, test_data, train_labels, test_labels, objectid, label, rebinning,
                                      int(nodes))

        # Save data
        with open(targetdir + learntype + rebinning + '.txt', 'a') as accfile:
            accfile.write("Accuracy: " + str(objectid) + "\n" + str(accuracylist) + '\n_________________________\n')

        # Plot 3D colorcolor
        Plotting.plotccd(objectid, accuracylist, test_obs, objecttype, targetdir, colorpath)
