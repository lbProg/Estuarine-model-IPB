import numpy as np

class Variable2d:
  def __init__(self, t, dim_x, dim_y, initial_value, name):
    self.value = np.full((len(t), dim_x, dim_y), initial_value, dtype = float)
    self.name = name