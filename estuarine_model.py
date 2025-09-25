import numpy as np

from tools import bathymetry
from tools import classes
from tools import visualization as visu
from tools import equations as eq

# Model parameters

model = classes.Model(
  t_0 = 0, # Initial time
  t_f = 2, # Max time (d)
  dt = 1 / 24 ,
  depth = 10,
  width = 10,
  res = 0.5
)

model.initialize_dims()

model.initialize_constants(
  N0 = 1, # nutrient input
  tau = 0.1 # turnover rate
)

# Define model variables

model.initialize_variables(
  light = classes.Variable2d(model, 0, "Light"),
  nutrients = classes.Variable2d(model, 0.1, "Nutrients"),
  phytoplankton = classes.Variable2d(model, 0.1, "Phytoplankton")
)

# Function to update model variables

def compute_variables(t, row, col, model):
  if (model.nrows - row > bathymetry.bathymetry(col)):
    model.light.update(t, row, col, eq.light(t, row, col, model))
    model.nutrients.value[t, row, col] = eq.nutrients(t, row, col, model)
    model.phytoplankton.value[t, row, col] = eq.nutrients(t, row, col, model)
  else :
    # No value underground
    model.light.value[t, row, col] = np.nan
    model.nutrients.value[t, row, col] = np.nan
    model.phytoplankton.value[t, row, col] = np.nan

# Model loop

for t in range(1, len(model.time)):
  for row in range(0, model.nrows):
    for col in range(0, model.ncols):
      compute_variables(t, row, col, model)

# Plor results in cross-section plot and line plots

visu.cross_plot(model.light, model)

# visu.line_plot(variables['light'], time)
