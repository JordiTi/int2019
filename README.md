# User guide 
## Folder overview
CreatePowerSpectra:
Scripts to create power spectra from files, structured the same as in
<https://heasarc.gsfc.nasa.gov/FTP/rxte/data/archive/>

LeaveOneOut:\
Scripts to read data, train machine learning algorithms on it and plot the results.

## Function overview
In CreatePowerSpectra in Powerspectrum.py:\
findPcaFileName():\
Finds the pca index file in the FMI file.

acceptmode():\
From a mode and time resolution in an observation, determines whether to accept this mode and time resolution.

binningFactor():\
Determine the rebinning factor for a given time resolution.

createPowerSpectrum():
From a path containing data and a path to the gti file, creates a power spectrum using WritePowerspectrum.sh.

getgtipath():\
Returns the gtipath if gtipath is in the folder of the object. 

main():\
From the path to all neutron star/black hole data, return powerspectra form files with the right mode and time 
resolution.

In LeaveOneOut in Data.py:\
loaddata():\
From the paths to the power spectra, loads the data.\

gettraindata():\
From the loaded data, pick data to train the algorithm.

In LeaveOneOut in LeaveOneOut.py:\
Main function, calls scripts to load data, preprocesses the data and calls functions to trian the algorithm and plot 
the results. 

In LeaveOneOut in Plotting.py:\
plotccd():\
Plots ccd from .color file with classification accuracy per power spectrum.

plotColorColor():\
Plots ccd from .color file.

In LeaveOneOut in Training.py:\
trainRF():\
Trains random forest classifier

trainNN():\
Trains neural network