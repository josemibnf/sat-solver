#!/bin/bash
VAR=true
RATIO=$2/$1
FICHERO="benchmark-folder/hardness-$1-$2-$3.cnf"
echo $FICHERO
((OPORTUNIDADES = $1 + $2))
while [[ "$VAR" == "true" && "$OPORTUNIDADES" != "0" ]]
do
    ./rnd-cnf-gen.py $1 $2 $3 > $FICHERO
    RESULT=$(minisat $FICHERO | tail -1)
    if [ $RESULT == "SATISFIABLE" ]; then
        VAR=false
    else
        ((OPORTUNIDADES = OPORTUNIDADES -1))
    fi
    echo $OPORTUNIDADES
done
if [[ "$OPORTUNIDADES" == "0" ]];then
    rm -f $FICHERO
fi