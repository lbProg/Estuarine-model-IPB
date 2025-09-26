import math

# Tracer for testing purposes

def tracer(value, model):
  return value[1:-1, 1:-1] + model.diff * model.dt * (
    (value[2:, 1:-1] - 2 * value[1:-1, 1:-1] + value[:-2, 1:-1]) / model.res**2 +
    (value[1:-1, 2:] - 2 * value[1:-1, 1:-1] + value[1:-1, :-2]) / model.res**2
  )

# Light availability

def light(t, row, col, model):
  periodicity = math.sin(2 * math.pi * t * model.dt) + 1 # 24-hour loop
  exponential_decay = 10 * math.exp(-0.3 * row * model.res)

  return periodicity * exponential_decay

# Nutrient concentration

def nutrients(t, row, col, model):
  previous_val = model.nutrients.value[t - 1, row, col]

  d = model.tau * (model.N0 - previous_val)

  return previous_val + d * model.dt

# Phytoplankton concentration

def phyto(t, row, col, model):
  previous_val = model.phytoplankton.value[t - 1, row, col]
  grazing = 0.1 * model.light.value[t - 1, row, col] * model.nutrients.value[t - 1, row, col]

  d = grazing - model.tau * previous_val

  return previous_val + d * model.dt

