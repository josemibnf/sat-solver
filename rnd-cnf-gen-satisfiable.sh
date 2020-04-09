#!/bin/bash
VAR=true
RATIO=$2/$1
FICHERO="benchmark-folder/hardness-$1-$2-$3.cnf"
echo $FICHERO
while $VAR
do
    ./rnd-cnf-gen.py $1 $2 $3 > $FICHERO
    RESULT=$(minisat $FICHERO | tail -1)
    if [ $RESULT == "SATISFIABLE" ]; then
        VAR=false
    fi
done