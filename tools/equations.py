import math
import numpy as np

# Tracer for testing purposes

def diffusion(value, model):
  return value[1:-1, 1:-1] + model.diff * (
    (value[2:, 1:-1] - 2 * value[1:-1, 1:-1] + value[:-2, 1:-1]) / model.res**2 +
    (value[1:-1, 2:] - 2 * value[1:-1, 1:-1] + value[1:-1, :-2]) / model.res**2
  ) * model.dt

def convection(value, model):
  dir = np.sign(model.constants["current"])

  x_mvt = np.roll(value, dir[0], axis = 1)
  y_mvt = np.roll(value, -dir[1], axis = 0)

  newval = value

  newval[1:-1, 1:-1] = (
    value[1:-1, 1:-1] - 10000 * model.dt / model.res * 
    (
      abs(model.constants["current"][0]) * (value[1:-1, 1:-1] - x_mvt[1:-1, 1:-1]) + 
      abs(model.constants["current"][1]) * (value[1:-1, 1:-1] - y_mvt[1:-1, 1:-1])
    )
  )

  # Set model borders to zero to avoid looping back over edges
  newval[0, :] = 0
  newval[:, 0] = 0
  newval[model.nrows + 1, :] = 0
  newval[:, model.ncols + 1] = 0

  return newval

# Light availability

def light(t, row, col, model):
  periodicity = math.sin(2 * math.pi * t * model.dt) + 1 # 24-hour loop
  exponential_decay = 10 * math.exp(-0.3 * row * model.res)

  return periodicity * exponential_decay

# Nutrient concentration

def nutrients(t, row, col, model):
  previous_val = model.nutrients.value[t - 1, row, col]

  d = model.tau * (model.N0 - previous_val)

  return previous_val + d * model.dt

# Phytoplankton concentration

def phyto(t, row, col, model):
  previous_val = model.phytoplankton.value[t - 1, row, col]
  grazing = 0.1 * model.light.value[t - 1, row, col] * model.nutrients.value[t - 1, row, col]

  d = grazing - model.tau * previous_val

  return previous_val + d * model.dt

