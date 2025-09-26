import numpy as np

from tools.classes import Variable2d, Model
from tools import visualization as visu
from tools import equations as eq

# Model parameters

model = Model(
  t_0 = 0, # Initial time
  t_f = 50, # Max time (d)
  depth = 100 * 20, # cm
  width = 100 * 20, # cm
  res = 10, # cm
  diff = 500 # Diffusion coefficient
)

model.initialize_dims()

model.initialize_constants(
  N0 = 1, # nutrient input
  tau = 0.1 # turnover rate
)

# Define model variables

tracer_init = np.fromfunction(
  lambda row, col: 
  np.where((row * model.res - model.depth/2)**2 + (col * model.res - model.width/2)**2 < 4E3 * model.res, 10, 0),
  (model.nrows, model.ncols)
)

model.initialize_variables({
  #"light": classes.Variable2d(model, 0, eq.light, "Light"),
  #"nutrients": classes.Variable2d(model, 0.1, eq.nutrients, "Nutrients"),
  #"phytoplankton": classes.Variable2d(model, 0.1, eq.phyto, "Phytoplankton")
  "tracer": Variable2d(model, tracer_init, eq.tracer, "Tracer")
})

print("--------------------")
model.summary()

# Model loop

for t in range(1, len(model.time)):
  model.do_timestep(t)

# Plor results in cross-section plot and line plots

# print(model.variables["tracer"].value)

visu.cross_plot(model.variables["tracer"], model)

# visu.line_plot(variables['light'], time)
