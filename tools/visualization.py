import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Cross-section plot to show x, y and time

def cross_plot(var, t_0, t_f, dt, rows, cols, res):
  max = np.nanmax(var.value)
  min = np.nanmin(var.value)

  # Create the figure
  fig, ax = plt.subplots()

  cmap = plt.cm.viridis
  cmap.set_bad('black')

  tile = plt.imshow(var.value[0, :, :], cmap = cmap, vmin = min, vmax = max)

  cbar = plt.colorbar(tile)
  cbar.ax.set_ylabel(var.name)
  cbar.ax.set_yticks(np.arange(min, max + (max - min) / 7, (max - min) / 6))

  ax.set_ylabel('Depth (m)')
  ax.set_xlim(0 - res / 2, cols - res / 2)
  ax.set_ylim(rows - res / 2, 0 - res / 2)

  ax.set_yticks(np.arange(0, rows, 1 / res))
  ax.set_yticklabels(np.arange(0, rows * res, 1).astype(int))

  ax.get_xaxis().set_visible(False)

  # adjust the main plot to make room for the slider
  fig.subplots_adjust(left = 0.25, bottom = 0.25)

  # Make a horizontal slider to control the time
  axtime = fig.add_axes([0.25, 0.1, 0.65, 0.03])
  time_slider = Slider(
      ax = axtime,
      label = 'Time (d)',
      valmin = t_0,
      valmax = t_f,
      valinit = t_0,
      valstep = dt
  )

  # The function to be called anytime a slider's value changes
  def update(t):
      t = int(t / dt)
      ax.imshow(var.value[t, :, :], cmap = cmap, vmin = min, vmax = max)
      fig.canvas.draw()

  # register the update function
  time_slider.on_changed(update)

  plt.show()