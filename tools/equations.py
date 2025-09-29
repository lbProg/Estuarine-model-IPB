import math
import numpy as np

# Advetion-diffusion equations

def diffusion(value, model):
  newval = value.copy()

  newval[1:-1, 1:-1] = value[1:-1, 1:-1] + model.diff * (
    (value[2:, 1:-1] - 2 * value[1:-1, 1:-1] + value[:-2, 1:-1]) / model.res**2 +
    (value[1:-1, 2:] - 2 * value[1:-1, 1:-1] + value[1:-1, :-2]) / model.res**2
  ) * model.dt

  return newval

def advection(value, model):
  # We can't directly use negative values for current (e.g. -1 on the x axis)
  # So we pre-compute forward and backward advection, and use the correct one for each
  # current value in the matrix

  # Forward and backward advection on v (side-by-side) and w (up-and-down) axes
  v_mvt_pos = np.roll(value, 1, axis = 1)
  v_mvt_neg = np.roll(value, -1, axis = 1)
  w_mvt_pos = np.roll(value, 1, axis = 0)
  w_mvt_neg = np.roll(value, -1, axis = 0)

  # Fetch values of v and w current flow for each cell
  flow_v = model.variables["flow_v"].value[model.iter, 1:-1, 1:-1]
  flow_w = model.variables["flow_w"].value[model.iter, 1:-1, 1:-1]

  newval = value.copy() # .copy() makes it not change the previous matrix (weird?)

  # For mass continuity, each cell should use the flow of the cell before for what it gains,
  # and the flow of itself (or the next cell ?) for what it loses (= transfer to next cell)
  # Lose your value * your flux and gain the value before * the flux before

  # Warning : current speed * model.adv * model.dt cannot be > 1
  # In one time step, no more that 100% of the content of a cell can be advected

  newval[1:-1, 1:-1] = (
    value[1:-1, 1:-1] +
    (
      (np.where(np.roll(flow_v, 1, axis = 1) > 0, np.roll(flow_v, 1, axis = 1), 0) * v_mvt_pos[1:-1, 1:-1]) - (np.where(flow_v > 0, flow_v, 0) * value[1:-1, 1:-1]) +
      (np.where(np.roll(flow_v, -1, axis = 1) < 0, np.roll(abs(flow_v), -1, axis = 1), 0) * v_mvt_neg[1:-1, 1:-1]) - (np.where(flow_v < 0, abs(flow_v), 0) * value[1:-1, 1:-1]) +
      (np.where(np.roll(flow_w, 1, axis = 0) > 0, np.roll(flow_w, 1, axis = 0), 0) * w_mvt_pos[1:-1, 1:-1]) - (np.where(flow_w > 0, flow_w, 0) * value[1:-1, 1:-1]) +
      (np.where(np.roll(flow_w, -1, axis = 0) < 0, np.roll(abs(flow_w), -1, axis = 0), 0) * w_mvt_neg[1:-1, 1:-1]) - (np.where(flow_w < 0, abs(flow_w), 0) * value[1:-1, 1:-1])
    ) * model.adv * model.dt
  )
  return newval

# Constant flow

def flow_const(value, model):
  return value

# Flow constant relative to initial value

def flow_const_init(value, model):
  matrix = value.copy()
  matrix[1:-1, 1:-1] = np.fromfunction(
    lambda row, col: 
    np.where(row < 5, -10, 0),
    (model.nrows, model.ncols)
  )

  return matrix

# Random flow everywhere

def flow_random(value, model):
  newval = value.copy()
  newval[1:-1, 1:-1] = np.random.rand(model.nrows, model.ncols) - 0.5
  
  return newval

# Periodic flow

def flow_period(value, model):
  newval = value.copy()
  newval[:, 0] = math.sin(model.t * 5) * 0.1 # Assign value on the border

  newval[1:-1, 1:-1] = newval[1:-1, 0]

  return newval

def flow_period2(value, model):
  newval = value.copy()
  newval[:, 0] = math.sin(model.t * 5 + math.pi/2) * 0.1 # Assign value on the border

  newval[1:-1, 1:-1] = newval[1:-1, 0]

  return newval

# Tracer for testing purposes

def tracer(value, model):
  return diffusion(advection(value, model), model)

# Light availability

def light(value, model):
  # periodicity = math.sin(2 * math.pi * model.t * model.dt) + 1 # 24-hour loop
  # exponential_decay = 10 * math.exp(-0.3 * model.row * model.res)

  light_matrix = np.ones((model.ncols + 2, model.nrows + 2)) * math.sin(model.t * 5)

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

