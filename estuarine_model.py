import numpy as np

from tools import bathymetry
from tools import classes
from tools import visualization as visu
from tools import equations as eq

# Model parameters

t_0 = 0 # Initial time
t_f = 2 # Max time (d)
dt = 1 / 12 # Time step (d), one time-step = 24/x hour

time = np.arange(t_0, t_f + dt, dt)

depth = 20
width = 20
res = 0.2

row_dims = int(depth / res)
col_dims = int(width / res)

# Define model variables

variables = {
  "light": classes.Variable2d(time, row_dims, col_dims, 0, "Light")
}

# Function to update model variables

def compute_variables(t, row, col, dt, variables):
  if (row_dims - row > bathymetry.bathymetry(col)) :
    variables['light'].value[t, row, col] = eq.light(t, row * res, col * res, dt, variables)
  else :
    # No value underground
    variables['light'].value[t, row, col] = np.nan

# Model loop

for t in range(0, len(time)) :
  for row in range(0, row_dims) :
    for col in range(0, col_dims) :
      compute_variables(t, row, col, dt, variables)

# Plor results in cross-section plot

visu.cross_plot(variables['light'], t_0, t_f, dt, row_dims, col_dims, res)
