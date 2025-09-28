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
      abs(row * (model.res / 100)- depth) + abs(col * (model.res / 100)- xpos) < side,
      10,
      0
    ),
    (model.nrows, model.ncols)
  )

  return matrix

def distribution_flow_uniform(model, left, right, top, bottom, val):
  matrix = np.full((model.nrows, model.ncols), val)

  return matrix

def distribution_flow(model, left, right, top, bottom, val):
  #matrix = np.full((model.nrows, model.ncols), val)
  # matrix = np.fromfunction(
  #   lambda row, col: row * val * 0.1, (model.nrows, model.ncols)
  # )
  # matrix = np.fromfunction(
  #   lambda row, col: np.where(col % 10 < 5, val * np.sign(row - 40), 0.5 * np.sign(row - 40)),
  #   (model.nrows, model.ncols)
  # )
  matrix = np.fromfunction(
    lambda row, col: np.where(col > 40, -1, 1), (model.nrows, model.ncols)
  )

  return matrix