# User guide 
## Folder overview
**Answerfiles:**\
Contains the files needed to create power spectra.

**CreatePowerSpectra:**\
Scripts to create power spectra from files

**LeaveOneOut:**\
Scripts to read data, train machine learning algorithms on it and plot the results.

**MakeGti:**\
Scripts to make the gti files and put them in a seperate folder

## Function overview
**In CreatePowerSpectra in WritePowerspectrum.sh**\
Changes the input files for fft and xana, then runs fft_xte

**In CreatePowerSpectra in Powerspectrum.py:**\
findPcaFileName():\
Finds the pca index file in the FMI file.

acceptmode():\
From a mode and time resolution in an observation, determines whether to accept this mode and time resolution.

binningFactor():\
Determine the rebinning factor for a given time resolution.

createPowerSpectrum():
From a path containing data and a path to the gti file, creates a power spectrum using WritePowerspectrum.sh.

getgtipath():\
Returns the gtipath if gti file is in the folder of the object. 

main():\
From the path to all neutron star/black hole data, return powerspectra form files with the right mode and time 
resolution.

**In LeaveOneOut in Data.py:**\
loaddata():\
From the paths to the power spectra, loads the data.\

gettraindata():\
From the loaded data, pick data to train the algorithm.

**In LeaveOneOut in LeaveOneOut.py:**\
Main function, calls scripts to load data, preprocesses the data and calls functions to trian the algorithm and plot 
the results. 

**In LeaveOneOut in Plotting.py:**\
plotccd():\
Plots ccd from .color file with classification accuracy per power spectrum.

plotColorColor():\
Plots ccd from .color file.

**In LeaveOneOut in Training.py:**\
trainRF():\
Trains random forest classifier

trainNN():\
Trains neural network

## How to create power spectra 
Before creating the power spectra, good time interval (gti) files are needed. These are 
created by the scripts in the MakeGti folder. These scripts also make files needed
for plotting.

In order to make the gti files, the data should be structured in the following way:\
main folder (NS or BH) containing either all NS or all BH data.\
|_Folders with objectid's\
|__Folders with observations for that objectid

First run makedirs.sh with a target directory flag. This target directory
is the path to the main folder. The script creates colorBH or colorNS folders.\
Second run coloranalysis.sh with a target directory flag. Also this flag
is the path to the main folder.\
Before copying the color files to a seperate folder make sure to change the following:\
In copycolor.py change the colordestination to the ./color/ folder and change 
the maindirectory path to the main folder. \
Finally run copycolor.py. The color files are now moved to the right folder.

Creating powerspectra is done with the scripts in the CreatePowerSpectra folder. \
Before running the Powerspectrum.py:
- In WritePowerspectrum.sh, replace the paths to the answerfiles with the right paths.
- In Powerspectrum.py, change the path in the main() function to the main path
- Make sure the gti file is in the folder of the objectid

Now run Powerspectrum.py and powerspectra will be placed in the folders of the observations.

## How to train the machine learning algorithms
Training machine learning algorithms is done with the scripts in the LeaveOneOut folder.\
One source is taken out as test data, and is classified based on the training data that gets used.

Before training make sure the data is structured in the following way:\
Objecttype\
|_ObjectID\
|__All powerspectra of this objectID (containing only the powers and 1 power per row)\
Also make sure there is a folder containing all .color files from color_analysis in the form objectid.color

Before training also make sure:
- In LeaveOneOut.py change the nsPath and bhPath to the paths pointing at the Objecttype folder
- In LeaveOneOut.py change the targetdir to the directory where the data can be saved
- In LeaveOneOut.py change the colorpath to the folder containing all .color files
- In Training.py change the parameters of the machine learning algorithms according to preference

Now run LeaveOneOut.py AlgorithmFlag RebinningFlag NumberOfPowers\
Where:
- AlgorithmFlag = the algorithm you want to run (RF for random forest or NN for neural network)
- RebinningFlag = the rebinning factor of the power spectra
- NumberOfPowersFlag = the number of powers per files

e.g. LeaveOneOut.py NN -30 109