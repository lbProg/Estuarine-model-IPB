import numpy as np

from tools import bathymetry
from tools import classes
from tools import visualization as visu
from tools import equations as eq

# Model parameters

t_0 = 0 # Initial time
t_f = 2 # Max time (d)
dt = 1 / 24 # Time step (d), one time-step = 24/x hour

time = np.arange(t_0, t_f + dt/2, dt)

depth = 10
width = 10
res = 0.5

row_dims = int(depth / res)
col_dims = int(width / res)

# Define model variables

variables = {
  "tau": 0.1, # turnover rate
  "N0": 1, # nutrient input
  "light": classes.Variable2d(time, row_dims, col_dims, 0, "Light"),
  "nutrients": classes.Variable2d(time, row_dims, col_dims, 0.1, "Nutrients"),
  "phytoplankton": classes.Variable2d(time, row_dims, col_dims, 0.1, "Phytoplankton")
}

# Function to update model variables

def compute_variables(t, row, col, res, dt, variables):
  if (row_dims - row > bathymetry.bathymetry(col)):
    variables['light'].update(t, row, col, eq.light(t, row, col, res, dt, variables))
    variables['nutrients'].value[t, row, col] = eq.nutrients(t, row, col, res, dt, variables)
    variables['phytoplankton'].value[t, row, col] = eq.nutrients(t, row, col, res, dt, variables)
  else :
    # No value underground
    variables['light'].value[t, row, col] = np.nan
    variables['nutrients'].value[t, row, col] = np.nan
    variables['phytoplankton'].value[t, row, col] = np.nan

# Model loop

for t in range(1, len(time)):
  for row in range(0, row_dims):
    for col in range(0, col_dims):
      compute_variables(t, row, col, res, dt, variables)

# Plor results in cross-section plot and line plots

visu.cross_plot(variables['light'], t_0, t_f, dt, row_dims, col_dims, res)

# visu.line_plot(variables['light'], time)
