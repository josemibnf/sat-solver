#!/bin/bash
# Ejecuta race.py para todo los benchmarks con todo los solvers, y los clasifica de mejor a peor.

SOLVERS=solvers/* # Directorio que contiene los solvers a evaluar
BENCHMARKS=benchmark-folder/ # Directorio que contiene los benchmarks que realizar

chmod 777 $SOLVERS
touch tmp-rating.txt

for s in $SOLVERS
do

  # Seleccionar el nombre del solver (lo siento)
  solver_name=$(echo $s | cut --complement -d/ -f 1 | cut -d. -f 1)

  echo "Rating $solver_name..."

  # Ejecuta race.py
  solver_time=$(./race.py $BENCHMARKS $s | grep "Total time =" | cut --complement -d= -f1)

  echo "$solver_name =$solver_time" >> tmp-rating.txt
done

echo -e "\n### Ranking ###\n"
cat tmp-rating.txt | sort -n -k3 -t" "
rm tmp-rating.txt