# Copy gtifiles into colors folder

import os
import shutil

def main():
    #directorystructure of main => NS/obsid/pca,fmi,fipc/measfiles
    mainDirectory = "/export/data/jordit/data/NS/"
    for objectid in os.listdir(mainDirectory):
        print("/export/data/jordit/data/NS/" + str(objectid))
        if os.path.exists("/export/data/jordit/data/NS/" + objectid + "/alldet_av_total_perobsid_clean.color"):
            print(objectid)
            gtifile = "/export/data/jordit/data/NS/" + objectid + "/alldet_av_total_perobsid_clean.color"
            destinationfile = "/export/data/jordit/data/colors/" + objectid + ".color"
            shutil.copy(gtifile, destinationfile)

main()
