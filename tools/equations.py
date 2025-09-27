import math
import numpy as np

def pad_zeros(matrix, model):
  matrix[0, :] = 0
  matrix[:, 0] = 0
  matrix[model.nrows + 1, :] = 0
  matrix[:, model.ncols + 1] = 0

  return matrix

# Advetion-diffusion equations

def diffusion(value, model):
  newval = value.copy()

  newval[1:-1, 1:-1] = value[1:-1, 1:-1] + model.diff * (
    (value[2:, 1:-1] - 2 * value[1:-1, 1:-1] + value[:-2, 1:-1]) / model.res**2 +
    (value[1:-1, 2:] - 2 * value[1:-1, 1:-1] + value[1:-1, :-2]) / model.res**2
  ) * model.dt

  # Set model borders to zero
  newval = pad_zeros(newval, model)

  return newval

def advection(value, model):
  dir = np.sign(model.constants["current"])

  x_mvt = np.roll(value, dir[0], axis = 1)
  y_mvt = np.roll(value, -dir[1], axis = 0)

  newval = value.copy() # .copy() makes it not change the previous matrix (weird?)

  newval[1:-1, 1:-1] = (
    value[1:-1, 1:-1] - model.adv * model.dt / model.res * 
    (
      abs(model.constants["current"][0]) * (value[1:-1, 1:-1] - x_mvt[1:-1, 1:-1]) + 
      abs(model.constants["current"][1]) * (value[1:-1, 1:-1] - y_mvt[1:-1, 1:-1])
    )
  )

  # Set model borders to zero to avoid looping back over edges
  newval = pad_zeros(newval, model)

  return newval

# Tracer for testing purposes

def tracer(value, model):
  return diffusion(advection(value, model), model)

# Light availability

def light(value, model):
  # periodicity = math.sin(2 * math.pi * model.t * model.dt) + 1 # 24-hour loop
  # exponential_decay = 10 * math.exp(-0.3 * model.row * model.res)

  light_matrix = np.ones((model.ncols + 2, model.nrows + 2)) * math.sin(model.t)
  light_matrix = pad_zeros(light_matrix, model)

  return light_matrix

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

