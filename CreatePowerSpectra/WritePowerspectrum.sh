#!/usr/bin/env bash

cd $1

# Change input filename
sed -i "2s/.*/${2}/" ./fftans.txt

#Apply .gti file
sed -i "4s/.*/Y/" ./fftans.txt

# Specify gti file directory
sed -i "5s/.*/${5}/" ./fftans.txt

# Specify gti file
sed -i "6s/.*/*rgedgti.txt/" ./fftans.txt

# Change output filename
sed -i "12s/.*/${3}.tra/" ./fftans.txt

# Change binning factor
sed -i "13s/.*/${4}/" ./fftans.txt

echo "FFT done"

# Change input filename
sed -i "2s/.*/${3}.tra/" ./xanaans.txt

# Change output filename
sed -i "18s/.*/${3}.asc/" ./xanaans.txt

xana < ./xanaans.txt

echo "XANA done"
