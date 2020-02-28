#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import subprocess
import argparse
import os.path
from os import listdir

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
    args = parser.parse_args()

    if args.maker is not False:
        solver = 'solvers/'+args.maker
        isSat(solver)
        subprocess.check_call(['./makesat.sh', solver])
        subprocess.run(['bash', 'makeplot.sh'])
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
