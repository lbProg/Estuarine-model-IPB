import math
import numpy as np
import matplotlib.pyplot as plt

# Paramètres du modèle

n_years = 5

t_0 = 0 # Initial time
t_f = 365 * n_years # Max time
dt = 2 # Time step (days ?)

time = np.arange(t_0, t_f + dt, dt)

# Variables

growth_P = 1.2
growth_Z = 0.6

mortality_Z = 0
mortality_P = 0

d_P = 0.2 # decomposition efficiency of dead phyto
d_Z = 0.2

e = 0.01 # Excretion rate of zoo

k_P_N = 2 # Phyto affinity for nutrients
k_Z_P = 10 # Zoo affinity for phyto

tau = 0.1 # System turnover rate

N0 = 1 # Nutrient input

# Valeurs initiales

init_N = 0.5
init_P = 0.2
init_Z = 0.2

N = [init_N] + [0] * (len(time) - 1)
P = [init_P] + [0] * (len(time) - 1)
Z = [init_Z] + [0] * (len(time) - 1)

# Stockage des variables

runoff_data = [0] * len(time)

# Run the model

for t in range(1, len(time)) :

  # Variables

  grazing = growth_P * (N[t - 1] / (k_P_N + N[t - 1])) * P[t - 1]
  predation = growth_Z * (P[t - 1] / k_Z_P) / (1 + P[t - 1] / k_Z_P)

  m_P = mortality_P * P[t - 1]
  m_Z = mortality_Z * Z[t - 1]

  runoff_max = (90/365 * math.pi/2) # 90 days = march
  runoff = 0.5 * math.sin(2 * math.pi / 365 * t * dt - runoff_max) + 0.6

  N0 = runoff # Nutrient input depends on runoff (?)

  # Differential equations

  dN_dt = predation * e + tau * (N0 - N[t - 1]) - grazing + m_P * d_P + m_Z * d_Z
  dP_dt = grazing - tau * P[t - 1] - m_P - predation
  dZ_dt = predation - tau * Z[t - 1] - m_Z

  N[t] = N[t - 1] + dN_dt * dt
  P[t] = P[t - 1] + dP_dt * dt
  Z[t] = Z[t - 1] + dZ_dt * dt

  N[t] = np.clip(N[t], 0, None)
  P[t] = np.clip(P[t], 0, None)
  Z[t] = np.clip(Z[t], 0, None)

  runoff_data[t] = runoff

  print(
    "Time : " + str(round(t, 3)) + 
    " | N : " + str(round(N[t], 3)) + 
    " | P : " + str(round(P[t], 3)) +
    " | Z : " + str(round(Z[t], 3)) +
    " | Runoff : " + str(round(runoff, 3))
  )

# Plot results

year_starts = range(1, t_f + 1, 365)

plt.close()

fig, ax = plt.subplots(2, sharex = True, height_ratios=(0.6, 0.4))

ax[0].plot(time, N, "r--", label = "Nutrients")
ax[0].plot(time, P, "g--", label = "Phytoplankton") 
ax[0].plot(time, Z, "b--", label = "Zooplankton")

ax[1].plot(time, runoff_data, label = "Runoff")

ax[0].legend()
ax[1].legend()

ax[1].set_xticks(year_starts)

plt.show()