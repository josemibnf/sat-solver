#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import subprocess
import argparse
import os
from os import listdir
import sys

def isSat(solver):
    if os.path.isfile(solver):
        return True
    else:
        print("ERROR: SOLVER    "+solver+"    NO ENCONTRADO.")
        sat_list = [f for f in listdir('./solvers') if os.path.isfile(os.path.join('./solvers', f))]
        print("Elige uno:  ", sat_list)
        exit()
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maker", "-m", help="do new experiment", default=False, action='store')
    parser.add_argument("--config", "-c", help="change configuration, en formato [,,,]", default=False, action='store')
    args = parser.parse_args()
    configuracion=[20, 80, 5, 5] #primera clausula, ultima clausula, numero de variables, numero de iteraciones.
    if args.config is not False:
            configuracion = args.config
    if args.maker is not False:
        solver = 'solvers/'+args.maker
        isSat(solver)
        #subprocess.check_call(['./makesat.sh', solver, str(configuracion[0]), str(configuracion[1]), str(configuracion[2]), str(configuracion[3])])
        subprocess.check_call(['./makeplot.sh', str(configuracion[0]), str(configuracion[1])])
    elif os.path.isdir('experiment') == False  or  os.path.isfile('experiment/res.txt') == False :
        print("Error: EXPERIMENTO INCOMPLETO, HAZ --maker")
        sat_list = [f for f in listdir('./solvers') if os.path.isfile(os.path.join('./solvers', f))]
        print("Elige uno:  ", sat_list)
        exit()

    data = pd.read_csv('experiment/res.txt', header=None)
    df = pd.DataFrame(data)
    x=df.index.tolist()
    y=df[0].tolist()
    plt.plot( x, y)
    plt.show()
