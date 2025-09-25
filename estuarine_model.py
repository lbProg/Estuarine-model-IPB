import math
import matplotlib.pyplot as plt
import numpy as np

from tools import bathymetry
from tools import classes
from tools import visualization as visu

# Model parameters

t_0 = 0 # Initial time
t_f = 2 # Max time (days)
dt = 1 / 24 # Time step (days)

time = np.arange(t_0, t_f + dt, dt)

depth = 10
width = 20
res = 0.5

row_dims = int(depth / res)
col_dims = int(width / res)

light = classes.Variable2d(time, row_dims, col_dims, 0, "Light")

# Model loop

for t in range(0, len(time)) :
  for row in range(0, row_dims) :
    for col in range(0, col_dims) :
      if (row_dims - row > bathymetry.bathymetry(col)) :
        light.value[t, row, col] = (math.sin(2 * math.pi / 10 * t) + 1) * (1 - row / row_dims)
      else :
        light.value[t, row, col] = np.nan

plt.close()

plot = visu.cross_plot(light, t_0, t_f, dt, row_dims, col_dims, res)