#!/bin/bash
cd experiment
for clauses in {200..800}
do
    echo "Clausula $clauses."
    let "clauses++"
    let "iter = 0"
    grep -c ^SATISFIABLE $clauses.txt >> res.txt
done