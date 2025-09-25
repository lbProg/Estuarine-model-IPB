import math

# Light availability

def light(t, row, col, dt, variables):
  periodicity = (math.sin(2 * math.pi * t * dt) + 1) # 24-hour loop
  exponential_decay = 10 * math.exp(-0.3 * row)

  return periodicity * exponential_decay