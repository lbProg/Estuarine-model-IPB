import math

# Light availability

def light(t, row, col, res, dt, vars):
  periodicity = (math.sin(2 * math.pi * t * dt) + 1) # 24-hour loop
  exponential_decay = 10 * math.exp(-0.3 * row * res)

  return periodicity * exponential_decay

def nutrients(t, row, col, res, dt, vars):
  previous_val = vars["nutrients"].value[t - 1, row, col]

  d = vars["tau"] * (vars["N0"] - previous_val)

  return previous_val + d * dt

def phytoplankton(t, row, col, res, dt, vars):
  previous_val = vars["phytoplankton"].value[t - 1, row, col]
  grazing = 0.1 * vars["light"].value[t - 1, row, col] * vars["nutrients"].value[t - 1, row, col]

  d = grazing - vars["tau"] * previous_val

  return previous_val + d * dt

