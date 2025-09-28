import numpy as np
import math

from tools.progressbar import progressbar
from tools import visualization as visu

class Model:
  def __init__(self, t_0, t_f, depth, width, res, diff, adv):
    self.t_0 = t_0
    self.t_f = t_f
    self.t = t_0
    self.iter = 0
    self.depth = depth
    self.width = width
    self.res = res
    self.diff = diff
    self.adv = adv

  def initialize_dims(self):
    # For stability purposes, we set dt to depend on the model resolution
    # If a tracer diffuses in space more than the model resolution, it glitches
    self.dt = 0.9 * self.res / (self.diff + self.adv)
    # self.dt = 0.02

    self.time = np.arange(self.t_0, self.t_f + self.dt / 2, self.dt)
    self.nrows = int(self.depth / self.res)
    self.ncols = int(self.width / self.res)

  def initialize_constants(self, constants):
    self.constants = constants

  def initialize_variables(self, variables):
    self.variables = variables

  def run(self, debug = False):
    if debug:
      self.summary()

    for t in range(1, len(self.time)):
      self.do_timestep(t)

      if debug:
        progressbar(t, len(self.time) - 1)

    if debug:
      print("")

  def do_timestep(self, t):
    self.t += self.dt
    self.iter += 1
    for var in self.variables.values():
      var.update(self, t)

  def summary(self):
    print(
      "\n########## MODEL SUMMARY ##########\n" +
      "Running model for " + str(self.t_f - self.t_0) + " days. " +
      "Total timesteps: " + str(len(self.time)) + "\n" +
      "Model dimensions: " + str(self.width / 100) +
      "m wide by " + str(self.depth / 100) + "m deep, " +
      "resolution of " + str(self.res) + "cm" + "\n" +
      "Total number of cells: " + str(self.nrows * self.ncols) + "\n" +
      "Variables monitored: " + str([i for i in self.variables]) + "\n"
    )
  
  def plot_results(self, var):
    return visu.plot(self.variables[var], self)