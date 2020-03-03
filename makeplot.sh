#!/bin/bash
# $1 primera clausula, $2 segunda clausula
cd experiment
clauses=$1
while [ "$clauses" -le "$2" ]
do
    echo "Clausula $clauses."
    let "clauses++"
    grep -c ^SATISFIABLE $clauses.txt >> res.txt
done
exit 0