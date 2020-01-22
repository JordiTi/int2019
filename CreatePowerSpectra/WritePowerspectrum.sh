#!/usr/bin/env bash

cd $1

# Change input filename
sed -i "2s/.*/${2}/" /export/data/jordit/code/colortopower/fftans.txt

#Apply .gti file
sed -i "4s/.*/Y/" /export/data/jordit/code/colortopower/fftans.txt

# Specify gti file directory
sed -i "5s/.*/${5}/" /export/data/jordit/code/colortopower/fftans.txt

# Specify gti file
sed -i "6s/.*/*rgedgti.txt/" /export/data/jordit/code/colortopower/fftans.txt

# Change output filename
sed -i "12s/.*/${3}.tra/" /export/data/jordit/code/colortopower/fftans.txt

# Change binning factor
sed -i "13s/.*/${4}/" /export/data/jordit/code/colortopower/fftans.txt

#fft_xte < /export/data/jordit/code/colortopower/fftans.txt

echo "FFT done"

# Change input filename
sed -i "2s/.*/${3}.tra/" /export/data/jordit/code/colortopower/xanaans.txt

# Change output filename
sed -i "18s/.*/${3}.asc/" /export/data/jordit/code/colortopower/xanaans.txt

xana < /export/data/jordit/code/colortopower/xanaans.txt

echo "XANA done"
