#!/usr/bin/python3

import sys
import os
import subprocess
import random

os.system("rm -r benchmark-folder/*")
try:
    while 1:
        rnd_cnf = "./rnd-cnf-gen-satisfiable.sh "+str(random.randrange(1,999))+" "+str(random.randrange(1,999))+" 3"
        subprocess.call(rnd_cnf, shell=True)
except KeyboardInterrupt:
    pass

os.system("./rate-solvers.sh")
