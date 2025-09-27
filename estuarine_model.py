from classes.model import Model
from classes.variable2d import Variable2d
from tools import equations as eq
from tools import initial_distributions as ini
from tools.visualization import visualize_results

# Model setup
model = Model(
  t_0 = 0, # Initial time (d)
  t_f = 3, # Max time (d)
  depth = 100 * 20, # cm
  width = 100 * 20, # cm
  res = 50, # Spatial resolution (cm)
  diff = 1000, # Diffusion coefficient (what unit ?)
  adv = 5000 # Advection coefficient (what unit ?)
)

model.initialize_dims()

model.initialize_constants({
  "N0": 1, # nutrient input
  "tau": 0.1, # turnover rate
  "current": (-0.1, 0.1) # Water flow vector, axes x-y
})

# Define model variables
tracer_init = ini.distribution_square(model, 10, 15, 30)

model.initialize_variables({
  "light": Variable2d(model, 0, eq.light, "Light"),
  #"nutrients": classes.Variable2d(model, 0.1, eq.nutrients, "Nutrients"),
  #"phytoplankton": classes.Variable2d(model, 0.1, eq.phyto, "Phytoplankton")
  "tracer_1": Variable2d(model, tracer_init, eq.tracer, "Tracer 1"),
  # "tracer_2": Variable2d(model, tracer_init, eq.convection, "Tracer 2"),
})

# Run the model
model.run(debug = True)

# Plor results in cross-section plot
visualize_results([model]) # As a list so you can put several different models and compare them