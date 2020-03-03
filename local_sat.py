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

def validConfig(config):
    return True

def beIgnored(experiment):
    ignore = open(".gitignore", "a")
    ignore.write("\n"+experiment+"/")
    ignore.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--maker", "-m", help="do new experiment", default=False, action='store')
    parser.add_argument("--config", "-c", help="change configuration", default=False, action='store', nargs='*')
    parser.add_argument("--experiment","-e", help="experiment directory", default=False, action='store')
    args = parser.parse_args()
    configuracion=[200, 800, 50, 3, 50] #primera clausula, ultima clausula, numero de variables, variables/clausula, numero de iteraciones.
    experiment='experiment' #by default
    if args.config is not False and validConfig(args.config):
        configuracion = args.config
    if args.experiment is not False:
        experiment = args.experiment
        beIgnored(experiment)
    if args.maker is not False:
        solver = 'solvers/'+args.maker
        isSat(solver)
        subprocess.check_call(['./makesat.sh', solver, str(configuracion[0]), str(configuracion[1]), str(configuracion[2]), str(configuracion[3]), str(configuracion[4]),experiment])
        subprocess.check_call(['./makeplot.sh', str(configuracion[0]), str(configuracion[1]), experiment])
    elif os.path.isdir(experiment) == False  or  os.path.isfile(experiment+'/res.txt') == False :
        print("Error: EXPERIMENTO INCOMPLETO, HAZ --maker")
        sat_list = [f for f in listdir('./solvers') if os.path.isfile(os.path.join('./solvers', f))]
        print("Elige uno:  ", sat_list)
        exit()

    data = pd.read_csv(experiment+'/res.txt', header=None)
    df = pd.DataFrame(data)
    x=df.index.tolist()
    y=df[0].tolist()
    plt.plot( x, y)
    plt.show()
