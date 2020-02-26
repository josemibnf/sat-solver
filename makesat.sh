#!/bin/bash
let "vars = 100"
let "clauses = 200"
rm -r experiment
mkdir experiment
for clauses in {200..800}
do
    echo "\n\n\n------------------------------"
    echo "Clausula $clauses."
    echo "------------------------------\n"
    let "clauses++"
    let "iter = 0"
    for i in {0..49}
    do
        let "iter++"

        python3 rnd-cnf-gen.py 50 $clauses 3 $i  | ./minisat >> experiment/$clauses.txt
    done
    rm cnf.cnf
done