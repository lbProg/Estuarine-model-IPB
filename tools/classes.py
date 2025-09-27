import numpy as np
from tools import bathymetry

class Variable2d:
  def __init__(self, model, initial_value, equation, name):
    self.value = np.zeros(
      (len(model.time), model.nrows, model.ncols), dtype = float
    )
    self.value[0, :, :] = initial_value
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
  def __init__(self, t_0, t_f, depth, width, res, diff):
    self.t_0 = t_0
    self.t_f = t_f
    self.depth = depth
    self.width = width
    self.res = res
    self.diff = diff

  def initialize_dims(self):
    # For stability purposes, we set dt to depend on the model resolution
    # If a tracer diffuses in space more than the model resolution, it glitches
    # self.dt = self.res / self.diff * 2.5
    self.dt = 0.001

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

  def summary(self):
    print(
      "Running model for " + str(self.t_f - self.t_0) + " days. " +
      "Total timesteps: " + str(len(self.time)) + "\n" +
      "Model dimensions: " + str(self.width / 100) +
      "m wide by " + str(self.depth / 100) + "m deep, " +
      "resolution of " + str(self.res) + "cm" + "\n" +
      "Total number of cells: " + str(self.nrows * self.ncols) + "\n" +
      "Variables monitored: " + str([i for i in self.variables])
    )