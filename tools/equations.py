import math

# Light availability

def light(t, row, col):
  periodicity = (math.sin(2 * math.pi / 24 * t) + 1)
  exponential_decay = 10 * math.exp(-0.6 * row)
  
  return periodicity * exponential_decay