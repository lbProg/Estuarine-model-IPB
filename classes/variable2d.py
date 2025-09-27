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

  def pad_zeros(self, matrix, model):
    # Set borders to zero to avoid weird behaviour like looping over edges.
    # The borders are not displayed and not taken into account in any way

    new_matrix = matrix.copy()

    new_matrix[0, :] = 0
    new_matrix[:, 0] = 0
    new_matrix[model.nrows + 1, :] = 0
    new_matrix[:, model.ncols + 1] = 0

    return new_matrix

  def update(self, model, t):
    self.value[t, :, :] = self.pad_zeros(
      self.equation(self.value[t - 1, :, :], model), model
    )
    