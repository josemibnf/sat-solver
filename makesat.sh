#!/bin/bash
#$1 solver, $2 primera clausula, $3 ultima clausula, $4 numero de variables, $5 numero de iteraciones
rm -r experiment
mkdir experiment
clauses=$2
while [ "$clauses" -le "$3" ]
do
    echo "\n\n\n------------------------------"
    echo "Clausula $clauses."
    echo "------------------------------\n"
    let "clauses++"
    i=0
    while [ "$i" -le "$5" ]
    do
        python3 rnd-cnf-gen.py $4 $clauses 3 $i > experiment/cnf.cnf
        ./$1 experiment/cnf.cnf >> experiment/$clauses.txt
        let "i++"
    done
done
exit 0