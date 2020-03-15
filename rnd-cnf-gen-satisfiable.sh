#!/bin/bash
VAR=true
FICHERO="benchmark-folder/hardness-$($2/$1)_$1-$2-$3.cnf"
echo $FICHERO
while $VAR
do
    ./rnd-cnf-gen.py $1 $2 $3 > $FICHERO
    RESULT=$(minisat $FICHERO | tail -1)
    echo $RESULT
    if [ $RESULT == "SATISFIABLE" ]; then
        VAR=false
    fi
done