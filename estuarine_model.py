import numpy as np

from tools.classes import Variable2d, Model
from tools import visualization as visu
from tools import equations as eq

# Model parameters

model = Model(
  t_0 = 0, # Initial time
  t_f = 10, # Max time (d)
  depth = 100 * 20, # cm
  width = 100 * 20, # cm
  res = 100, # cm
  diff = 1000 # Diffusion coefficient
)

model.initialize_dims()

model.initialize_constants(
  N0 = 1, # nutrient input
  tau = 0.1 # turnover rate
)

# Define model variables

tracer_init = np.fromfunction(
  lambda row, col: 
  np.where((row * model.res - model.depth/2)**2 + (col * model.res - model.width/2)**2 < 2E3 * model.res, 10, 0),
  (model.nrows, model.ncols)
)

tracer_init_2 = np.fromfunction(
  lambda row, col: 
  np.where((row * model.res - model.depth/2)**2 + (col * model.res - model.width/2)**2 < 2E3 * model.res, 10, 0),
  (model.nrows, model.ncols)
)

model.initialize_variables({
  #"light": classes.Variable2d(model, 0, eq.light, "Light"),
  #"nutrients": classes.Variable2d(model, 0.1, eq.nutrients, "Nutrients"),
  #"phytoplankton": classes.Variable2d(model, 0.1, eq.phyto, "Phytoplankton")
  "tracer_1": Variable2d(model, tracer_init, eq.convection, "Tracer 1"),
  "tracer_2": Variable2d(model, tracer_init_2, eq.diffusion, "Tracer 2")
})

print("--------------------")
model.summary()

# Model loop

for t in range(1, len(model.time)):
  model.do_timestep(t)

# Plor results in cross-section plot and line plots

# print(model.variables["tracer"].value)

visu.cross_plot(model.variables["tracer_1"], model)

# visu.line_plot(variables['light'], time)
