# Copy gtifiles into colors folder for NS data or BH data

import os
import shutil


def main():
    colordestination = "./colors/"
    mainDirectory = "./NS/"
    for objectid in os.listdir(mainDirectory):
        print("./NS/" + str(objectid))
        if os.path.exists(mainDirectory + objectid + "/alldet_av_total_perobsid_clean.color"):
            print(objectid)
            gtifile = mainDirectory + objectid + "/alldet_av_total_perobsid_clean.color"
            destinationfile = colordestination + objectid + ".color"
            shutil.copy(gtifile, destinationfile)

main()
