#!/usr/bin/env bash
# Make colorBH folders with @dirs.txt files in it
# targetdir = */NS/ or */BH/

targetdir=$1
for d in $targetdir*/ ; do
	touch ${d}@dirs.txt
	ls $d*/ -d > ${d}@dirs.txt
	head -n -2 ${d}@dirs.txt > temp.txt ; mv temp.txt ${d}@dirs.txt  
        if [[ $1 == */NS/ ]] ; then
                [[ -d ${d}colorNS ]] || mkdir ${d}colorNS
                cp ${d}@dirs.txt ${d}colorNS/
        fi
       	if [[ $1 == */BH*/ ]] ; then
                [[ -d ${d}colorBH ]] || mkdir ${d}colorBH
                cp ${d}@dirs.txt ${d}colorBH/
        fi
done

