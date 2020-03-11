#!/bin/bash
#$1 solver, $2 primera clausula, $3 ultima clausula, $4 numero de variables, $5 numero de iteraciones
rm -r $7
mkdir $7
clauses=$2
while [ "$clauses" -le "$3" ]
do
    echo "------------------------------"
    echo "Clausula $clauses."
    echo "------------------------------"
    let "clauses++"
    i=0
    while [ "$i" -le "$6" ]
    do
        python3 rnd-cnf-gen.py $4 $clauses $5 $i > $7/cnf.cnf
        ./$1 $7/cnf.cnf | grep "SATISFIABLE" >> $7/$clauses.txt
        let "i++"
    done
done
exit 0