import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import subprocess

#subprocess.run(['bash','makesat.sh'])
#subprocess.run(['bash','makeplot.sh'])

data = pd.read_csv('experiment/res.txt', header=None)
df = pd.DataFrame(data)
x=df.index.tolist()
y=df[0].tolist()
plt.plot( x, y)
plt.show()