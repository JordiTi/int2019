#!/usr/bin/env bash
# Perform color_analysis on all objects
# targetdir = */NS/ or */BH/
targetdir=$1
for d in $targetdir*/ ; do
        cd $d
        color_analysis < ./colorans.txt
done

