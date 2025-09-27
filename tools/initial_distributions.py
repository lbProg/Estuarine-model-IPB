import numpy as np

def distribution_circle(model, radius, depth, xpos):
  matrix = np.fromfunction(
    lambda row, col: 
    np.where(
      (row * (model.res / 100) - depth)**2 + (col * (model.res / 100) - xpos)**2 < radius,
      10,
      0
    ),
    (model.nrows, model.ncols)
  )

  return matrix

def distribution_square(model, side, depth, xpos):
  matrix = np.fromfunction(
    lambda row, col: 
    np.where(
      abs(row - depth) + abs(col - xpos) < side,
      10,
      0
    ),
    (model.nrows, model.ncols)
  )

  return matrix