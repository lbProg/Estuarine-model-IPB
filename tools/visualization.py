import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# Cross-section plot to show x, y and time

def cross_plot(var, model):
  global time, variable

  time = 1
  variable = var
  
  variable_dict = {
    "Light": model.light,
    "Nutrients": model.nutrients
  }

  max_var = np.nanmax(variable.value)
  min_var = np.nanmin(variable.value)

  # Create the figure
  fig, ax = plt.subplots()

  cmap = plt.cm.viridis
  cmap.set_bad('black')

  tile = plt.imshow(var.value[1, :, :], cmap = cmap, vmin = min_var, vmax = max_var)

  cbar = plt.colorbar(tile)
  cbar.ax.set_ylabel(var.name)

  ax.set_ylabel('Depth (m)')
  ax.set_xlim(0, model.ncols - model.res)
  ax.set_ylim(model.nrows - model.res, 0 - model.res)

  ax.set_yticks(np.arange(0, model.nrows, 1 / model.res))
  ax.set_yticklabels(np.arange(0, model.nrows * model.res, 1).astype(int))

  ax.get_xaxis().set_visible(False)

  # adjust the main plot to make room for the slider
  fig.subplots_adjust(left = 0.25, bottom = 0.25)

  # Make a horizontal slider to control the time
  axtime = fig.add_axes([0.25, 0.1, 0.65, 0.03])
  time_slider = Slider(
      ax = axtime,
      label = 'Time (d)',
      valmin = model.t_0,
      valmax = model.t_f,
      valinit = model.t_0 + model.dt,
      valstep = model.dt
  )

  # Choose variable
  axbuttons = fig.add_axes([0.01, 0.25, 0.2, 0.65])
  var_buttons = RadioButtons(
    axbuttons,
    labels = list(variable_dict.keys()),
    active = list(variable_dict.keys()).index(var.name)
  )

  # Update plot after user input
  def update_time(t):
    global time
    time = int(t / model.dt)
    update_plot(time, variable)
    
  def update_variable(v):
    global variable
    variable = variable_dict[v]
    update_plot(time, variable)

  def update_plot(time, variable):
    max_var = np.nanmax(variable.value)
    min_var = np.nanmin(variable.value)
    ax.imshow(variable.value[time, :, :], cmap = cmap, vmin = min_var, vmax = max_var)
    fig.canvas.draw()

  # register the update function
  time_slider.on_changed(update_time)
  var_buttons.on_clicked(update_variable)

  plt.show()

# Line plot to show a variable through time

def line_plot(var, time):
  values = var.value[:, :, :]
  sum_by_time = np.nansum(np.nansum(values, axis = 1), axis = 1)

  plt.close()

  ax = plt.subplot()

  ax.plot(time, sum_by_time, "r--", label = var.name)
  plt.legend()

  plt.show()