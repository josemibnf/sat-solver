#!/usr/bin/python3

import sys
import os
import subprocess
import random


if __name__ == '__main__':
    while 1:
        rnd_cnf = "./rnd-cnf-gen-satisfiable.sh "+str(random.randrange(1,999))+" "+str(random.randrange(1,999))+" 3"
        print(rnd_cnf)
        subprocess.call(rnd_cnf, shell=True)