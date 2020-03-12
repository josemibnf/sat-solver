#!/bin/bash

# Ejecuta race.py para todo los benchmarks con todo los solvers, y los clasifica de mejor a peor.

SOLVERS=solvers/*
BENCHMARKS=benchmark-folder/
chmod 777 $SOLVERS

touch tmp-rating

for s in $SOLVERS
do
  echo "Rating $s"

  # Lo siento, esto solo pilla el nombre del solver
  echo "" >> tmp-rating
  echo $s | cut --complement -d/ -f 1 | cut -d. -f 1 >> tmp-rating

  # Ejecuta race.py
  ./race.py $BENCHMARKS $s | grep "Total time =" >> tmp-rating

done

cat tmp-rating
rm tmp-rating
