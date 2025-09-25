import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Paramètres du modèle

t_0 = 0 # Initial time
t_f = 2 # Max time
dt = 1 # Time step (days ?)

time = np.arange(t_0, t_f + dt, dt)

x_range = 5
y_range = 5
res = 1

# Variables
Var = np.zeros((len(time), int(x_range / res), int(y_range / res)))

for t in range(0, len(time) - 1) :
  for x in range(0, Var.shape[1]) :
    for y in range(0, Var.shape[2]) :
      dVar_dt = 1

      Var[t, x, y] = Var[t - 1, x, y] + dVar_dt * dt


# def plot_slice(X):
#   plt.close()
#   fig, ax = plt.subplot()
#   ax.imshow(X[0, :, :])

#   plt.show()

# plot_slice(Var)

# plt.close()

# fig = plt.figure()
# ax = fig.add_subplot()

# axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])

# freq_slider = Slider(
#     ax=axfreq,
#     label='Frequency [Hz]',
#     valmin=0.1,
#     valmax=30,
#     valinit=5,
# )

# ax.imshow(Var[1, :, :])

# plt.show()

# plt.close()


plt.close()

fig, ax = plt.subplots(2, sharex = True, height_ratios=(0.6, 0.4))

ax[0].plot(time, Var[:, 0, 0], "r--", label = "Nutrients")

plt.show()