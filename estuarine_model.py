import numpy as np

from tools.classes import Variable2d, Model
from tools import visualization as visu
from tools import equations as eq

# Model parameters

model = Model(
  t_0 = 0, # Initial time
  t_f = 2, # Max time (d)
  dt = 1 / 24, # Time step (d), one time-step = 24/x hour
  depth = 10,
  width = 10,
  res = 0.5
)

model.initialize_dims()

model.initialize_constants(
  N0 = 1, # nutrient input
  tau = 0.1 # turnover rate
)

# Define model variables

tracer_init = np.fromfunction(lambda row, col: row, (model.nrows, model.ncols))

model.initialize_variables({
  #"light": classes.Variable2d(model, 0, eq.light, "Light"),
  #"nutrients": classes.Variable2d(model, 0.1, eq.nutrients, "Nutrients"),
  #"phytoplankton": classes.Variable2d(model, 0.1, eq.phyto, "Phytoplankton")
  "tracer": Variable2d(model, tracer_init, eq.tracer, "Tracer")
})

# Model loop

for t in range(1, len(model.time)):
  model.do_timestep(t)

# Plor results in cross-section plot and line plots

# print(model.variables["tracer"].value)

visu.cross_plot(model.variables["tracer"], model)

# visu.line_plot(variables['light'], time)