import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# Cross-section plot to show x, y and time

def cross_plot(var, model):
  global time, variable
  global values, sum_by_time

  time = 1
  variable = var
  
  # Make a dictionary with all model variables
  variable_dict = {}
  for i in model.variables:
    variable_dict[i.name] = i

  max_var = np.nanmax(variable.value)
  min_var = np.nanmin(variable.value)

  def update_line_plot():
    global values, sum_by_time

    values = variable.value[:, :, :]
    sum_by_time = np.nansum(np.nansum(values, axis = 1), axis = 1)
    
  update_line_plot()

  # Create the figure
  fig, axes = plt.subplots(2, 1, height_ratios = (0.7, 0.3))

  cmap = plt.cm.viridis
  cmap.set_bad('black')

  tile = axes[0].imshow(var.value[time, :, :], cmap = cmap, vmin = min_var, vmax = max_var)

  cbar = plt.colorbar(tile)
  cbar.ax.set_ylabel(var.name)

  axes[0].set_ylabel('Depth (m)')
  axes[0].set_xlim(0, model.ncols - model.res)
  axes[0].set_ylim(model.nrows - model.res, 0 - model.res)

  axes[0].set_yticks(np.arange(0, model.nrows, 1 / model.res))
  axes[0].set_yticklabels(np.arange(0, model.nrows * model.res, 1).astype(int))

  axes[0].get_xaxis().set_visible(False)

  axes[1].plot(model.time, sum_by_time, "r--", label = variable.name)
  axes[1].axvline(x = model.time[time])

  plt.legend()

  # adjust the main plot to make room for the slider
  fig.subplots_adjust(left = 0.3, bottom = 0.2)

  # Make a horizontal slider to control the time
  axtime = fig.add_axes([0.33, 0.1, 0.55, 0.03])
  time_slider = Slider(
      ax = axtime,
      label = 'Time (d)',
      valmin = model.t_0,
      valmax = model.t_f,
      valinit = model.t_0 + model.dt,
      valstep = model.dt
  )

  # Choose variable
  axbuttons = fig.add_axes([0, 0.25, 0.2, 0.65])
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
    axes[0].imshow(variable.value[time, :, :], cmap = cmap, vmin = min_var, vmax = max_var)
    cbar.ax.set_ylabel(variable.name)

    update_line_plot()
    axes[1].clear()
    axes[1].plot(model.time, sum_by_time, "r--", label = variable.name)
    axes[1].axvline(x = model.time[time])

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