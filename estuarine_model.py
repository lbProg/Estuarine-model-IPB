from classes.model import Model
from classes.variable2d import Variable2d
from tools import equations as eq
from tools import initial_distributions as ini
from tools.visualization import visualize_results

# Model setup
model = Model(
  t_0 = 0, # Initial time (d)
  t_f = 4, # Max time (d)
  depth = 100 * 40, # cm
  width = 100 * 40, # cm
  res = 50, # Spatial resolution (cm)
  diff = 1000, # Diffusion coefficient (what unit ?)
  adv = 5000 # Advection coefficient (what unit ?)
)

model.initialize_dims()

model.initialize_constants({
  "N0": 1, # nutrient input
  "tau": 0.1, # turnover rate
})

# Define model variables
tracer_init = ini.distribution_square(model, 5, 10, 10)
flow_v_init = ini.distribution_flow(model, 1, 0, 0, 0, val = -0.1)
flow_w_init = ini.distribution_flow(model, 0, 0, 0, 0, 0)

model.initialize_variables({
  "flow_v": Variable2d(model, flow_v_init, eq.flow_period, "Flow v"),
  "flow_w": Variable2d(model, flow_w_init, eq.flow_period2, "Flow w"),
  "tracer_1": Variable2d(model, tracer_init, eq.tracer, "Tracer 1")
  # "tracer_2": Variable2d(model, tracer_init, eq.convection, "Tracer 2"),
})

# Run the model
model.run(debug = True)

# Plor results in cross-section plot
visualize_results([model]) # As a list so you can put several different models and compare them