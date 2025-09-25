import numpy as np

class Variable2d:
  def __init__(self, model, initial_value, name):
    self.value = np.full(
      (len(model.time), model.nrows, model.ncols), initial_value, dtype = float
    )
    self.name = name

  def update(self, t, row, col, value):
    self.value[t, row, col] = value

class Model:
  def __init__(self, t_0, t_f, dt, depth, width, res):
    self.t_0 = t_0
    self.t_f = t_f
    self.dt = dt # Time step (d), one time-step = 24/x hour
    self.depth = depth
    self.width = width
    self.res = res

  def initialize_dims(self):
    self.time = np.arange(self.t_0, self.t_f + self.dt / 2, self.dt)
    self.nrows = int(self.depth / self.res)
    self.ncols = int(self.width / self.res)

  def initialize_constants(self, tau, N0):
    self.tau = tau
    self.N0 = N0

  def initialize_variables(self, light, nutrients, phytoplankton):
    self.light = light
    self.nutrients = nutrients
    self.phytoplankton = phytoplankton