# Plots ccds
import matplotlib.pyplot as plt
import numpy as np


# Plot ccd with accuracy
def plotccd(objectid, accuracylist, test_obs, objecttype, targetdir, colorpath):

    soft = []
    hard = []
    intens = []
    accuracy = []

    # Open colorfile and append softness/hardness/intensity/accuracy to lists
    with open(colorpath + str(objectid).strip() + ".color", 'r') as colorfile:
        for line in colorfile.readlines():
            time, softcolor, serror, hardcolor, herror, intensity, ierror, obsid = line.split()
            test_indices = [i for i, x in enumerate(test_obs) if x == obsid]

            if test_indices and 10 > float(hardcolor) > 0 and 10 > float(softcolor) > 0:
                acc = sum(accuracylist[test_indices])/len(test_indices)
                soft.append(float(softcolor))
                hard.append(float(hardcolor))
                intens.append(float(intensity))
                accuracy.append(float(acc))

        # Plot
        plt.figure(1)
        markersize = 30
        plt.title(str(objectid))
        plt.set_cmap('copper')
        if objecttype == "BH":
            plt.yscale('log')
            plt.xscale('log')
            plt.scatter(hard, intens, c=accuracy, s=markersize)
            plt.xlabel('hard')
            plt.ylabel('intensity')
        if objecttype == "NS":
            plt.xscale('linear')
            plt.yscale('linear')
            plt.scatter(soft, hard, c=accuracy, s=markersize)
            plt.xlabel('soft')
            plt.ylabel('hard')
        plt.clim(0, 1)
        a = plt.colorbar()
        a.set_label("Classification accuracy")
        plt.savefig(targetdir + str(objectid) + ".png")
        plt.close(1)


# Plot the colorcolor diagram
def plotColorColor(colorpath, objectid, objecttype):

    soft = []
    hard = []
    intens = []

    with open(colorpath, 'r') as colorfile:
        for line in colorfile.readlines():
            time, softcolor, serror, hardcolor, herror, intensity, ierror, obsid = line.split()
            if 10 > float(hardcolor) > 0 and 10 > float(softcolor) > 0:
                soft.append(float(softcolor))
                hard.append(float(hardcolor))
                intens.append(float(intensity))

        plt.figure(1)
        markersize = 20
        plt.title(str(objectid))
        if objecttype == "BH":
            plt.yscale('log')
            plt.xscale('log')
            plt.scatter(hard, intens, s=markersize,  color='royalblue')
            plt.xlabel('hard')
            plt.ylabel('intensity')
        if objecttype == "NS":
            plt.xscale('linear')
            plt.yscale('linear')
            plt.scatter(soft, hard, s=markersize,  color='royalblue')
            plt.xlabel('soft')
            plt.ylabel('hard')
        plt.savefig(str(objectid) + ".png")
        plt.close(1)


