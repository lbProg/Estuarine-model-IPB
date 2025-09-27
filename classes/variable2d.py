import numpy as np

from tools import bathymetry

class Variable2d:
  def __init__(self, model, initial_value, equation, name):
    self.value = np.zeros(
      (len(model.time), model.nrows + 2, model.ncols + 2), dtype = float
    )
    self.value[0, 1:-1, 1:-1] = initial_value
    self.equation = equation
    self.name = name

  # def update(self, t, row, col, model):
  #   if (model.nrows - row > bathymetry.bathymetry(col)):
  #     self.value[t, row, col] = self.equation(t, row, col, model)
  #   else:
  #     self.value[t, row, col] = np.nan

  def update(self, model, t):
    self.value[t, :, :] = self.equation(self.value[t - 1, :, :], model)