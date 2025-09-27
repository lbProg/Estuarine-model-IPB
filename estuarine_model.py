import numpy as np

from tools.classes import Variable2d, Model
from tools import equations as eq

# Model parameters

model = Model(
  t_0 = 0, # Initial time (d)
  t_f = 3, # Max time (d)
  depth = 100 * 20, # cm
  width = 100 * 40, # cm
  res = 50, # Spatial resolution (cm)
  diff = 1000, # Diffusion coefficient (what unit ?)
  conv = 5000 # Advection coefficient (what unit ?)
)

model.initialize_dims()

model.initialize_constants({
  "N0": 1, # nutrient input
  "tau": 0.1, # turnover rate
  "current": (-0.1, 0.1) # Water flow vector, axes x-y
})

# Define model variables

tracer_init = np.fromfunction(
  lambda row, col: 
  np.where(
    (row * model.res - model.depth/2)**2 + (col * model.res - model.width/2)**2 < 3E6 / model.res,
    10,
    0
  ),
  (model.nrows, model.ncols)
)

model.initialize_variables({
  #"light": classes.Variable2d(model, 0, eq.light, "Light"),
  #"nutrients": classes.Variable2d(model, 0.1, eq.nutrients, "Nutrients"),
  #"phytoplankton": classes.Variable2d(model, 0.1, eq.phyto, "Phytoplankton")
  "tracer_1": Variable2d(model, tracer_init, eq.tracer, "Tracer 1"),
  "tracer_2": Variable2d(model, tracer_init, eq.convection, "Tracer 2"),
})

# Model loop

model.run(debug = False)

# print(model.variables["tracer_1"].value[0, :, :])

# Plor results in cross-section plot and line plots

model.plot_results("tracer_1")
