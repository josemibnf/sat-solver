#!/bin/bash
let "clauses = 200"
rm -r experiment
mkdir experiment
for clauses in {200..800}
do
    echo "\n\n\n------------------------------"
    echo "Clausula $clauses."
    echo "------------------------------\n"
    let "clauses++"
    for i in {0..49}
    do
        python3 rnd-cnf-gen.py 50 $clauses 3 $i > experiment/cnf.cnf
        ./$1 experiment/cnf.cnf >> experiment/$clauses.txt
    done
done