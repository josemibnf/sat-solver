#!/bin/bash
VAR=true
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
done
if [[ "$OPORTUNIDADES" == "0" ]];then
    rm -f $FICHERO
    exit -1
fi