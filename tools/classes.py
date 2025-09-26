import numpy as np
from tools import bathymetry

class Variable2d:
  def __init__(self, model, initial_value, equation, name):
    # self.value = np.full(
    #   (len(model.time), model.nrows, model.ncols), initial_value, dtype = float
    # )
    self.value = initial_value
    self.equation = equation
    self.name = name

  # def update(self, t, row, col, model):
  #   if (model.nrows - row > bathymetry.bathymetry(col)):
  #     self.value[t, row, col] = self.equation(t, row, col, model)
  #   else:
  #     self.value[t, row, col] = np.nan

  def update(self, model, t):
    self.value[t, :, :] = self.equation(self.value[t - 1, :, :], model)

class Model:
  def __init__(self, t_0, t_f, dt, depth, width, res):
    self.t_0 = t_0
    self.t_f = t_f
    self.dt = dt
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

  def initialize_variables(self, variables):
    self.variables = variables

  def do_timestep(self, t):
    # self.var_copies = self.variables
    for var in self.variables.values():
      var.update(self, t)