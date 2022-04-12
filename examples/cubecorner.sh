#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

for i in {0..10}
do
  delta=$(( 2*$i ))
  $DIR/../vtk-unitcell.py \
    --axisangle 1 1 1 $(( 120/10*$i )) \
    --degrees \
    --family cubic \
    --position $delta $delta $delta \
  > cubecorner_$i.vtk

done
