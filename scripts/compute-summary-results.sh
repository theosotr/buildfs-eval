#! /bin/bash

rm -f $1/faults.csv
for project in $1/*; do
  name=$(basename $project)
  ov=$(cat $project/$name.faults |
    grep -oP 'OV\): [0-9]+' |
    sed -r 's/OV\): ([0-9]+)/\1/g')
  if [ -z $ov ]; then
    ov=0
  fi
  mn=$(cat $project/$name.faults |
    grep -oP 'MIN\): [0-9]+' |
    sed -r 's/MIN\): ([0-9]+)/\1/g')
  if [ -z $mn ]; then
    mn=0
  fi
  mout=$(cat $project/$name.faults |
    grep -oP 'MOUT\): [0-9]+' |
    sed -r 's/MOUT\): ([0-9]+)/\1/g')
  if [ -z $mout ]; then
    mout=0
  fi
  echo "$name,$mn,$mout,$ov" >> $1/faults.csv
done
