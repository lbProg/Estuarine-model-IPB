import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

class Plot:
  def __init__(self, initial_var, model):
    self.var = initial_var
    self.time = 1 # Start at first simulation step (don't show initial state)
    self.model = model
    self.cmap = plt.cm.viridis
    self.cmap.set_bad("black") # nan color
    self.tickres = model.nrows / 20 # One tick every n metres
    self.tick_factor = 100 # Conversion factor between rows (cm) and y axis (m)
    self.padding = 0 # Space around model

    self.get_initial_values()

  def get_initial_values(self):
    # Make a dictionary with all model variables
    self.var_names = {}
    for i in self.model.variables.values():
      self.var_names[i.name] = i

    self.vmin = np.nanmin(self.var.value)
    self.vmax = np.nanmax(self.var.value)

    # Colorbar is weird if no variation, so we artificially give it a range
    if (self.vmax == self.vmin):
      self.vmax += self.vmax / 10
      self.vmin -= self.vmin / 10

    self.update_line_plot_data()
    
  def update_line_plot_data(self):
    self.values = self.var.value[:, :, :]
    self.sum_by_time = np.nansum(np.nansum(self.values, axis = 1), axis = 1)

  def update_time(self, t):
    self.time = int(t / self.model.dt)
    self.update_plot()

  def update_var(self, v):
    self.var = self.var_names[v]

    self.vmin = np.nanmin(self.var.value)
    self.vmax = np.nanmax(self.var.value)

    # Colorbar is weird if no variation, so we artificially give it a range
    if (self.vmax == self.vmin):
      self.vmax += self.vmax / 10
      self.vmin -= self.vmin / 10

      print(self.vmax)

    # self.fig.delaxes(self.cbar.ax)
    # self.cbar = self.fig.colorbar(self.tile)
    # self.cbar.ax.set_ylabel(self.var.name)

    # gs = gridspec.GridSpec(1, 1)  # Recreate GridSpec without the colorbar space
    # self.axes[0].set_position(gs[0].get_position(self.fig))  # Adjust the position of the main plot
    # self.axes[0].set_subplotspec(gs[0])

    # self.fig.subplots_adjust(left = 0.3, bottom = 0.2)

    self.update_plot()

  def update_plot(self):
    # Update cross-section plot
    self.tile = self.axes[0].imshow(
      self.var.value[self.time, :, :], cmap = self.cmap, vmin = self.vmin, vmax = self.vmax
    )

    # Line for water level
    self.hline.remove()
    self.hline = self.axes[0].axhline(y = self.model.constants["water_level"][self.time] * 100 / self.model.res)

    # Update line plot
    self.update_line_plot_data()
    self.axes[1].clear()
    self.axes[1].plot(self.model.time, self.sum_by_time, "r--")
    self.axes[1].axvline(x = self.model.time[self.time])

    # Draw the new plots
    self.fig.canvas.draw()

  def set_axes(self):
    self.axes[0].set_ylabel('Depth (m)')
    self.axes[0].set_xlim(self.padding + 0.5, self.model.ncols - self.padding)
    self.axes[0].set_ylim(self.model.nrows - self.padding, self.padding + 0.5)

    self.axes[0].set_yticks(
      np.arange(0.5, self.model.nrows + 1, 1 / self.model.res * self.tick_factor * self.tickres)
    )
    self.axes[0].set_yticklabels(
      np.arange(0, (self.model.nrows + 1) * self.model.res / self.tick_factor, self.tickres).astype(int)
    )

    self.axes[0].set_xticks(
      np.arange(0.5, self.model.ncols + 1, 1 / self.model.res * self.tick_factor * self.tickres)
    )
    self.axes[0].set_xticklabels(
      np.arange(0, (self.model.ncols + 1) * self.model.res / self.tick_factor, self.tickres).astype(int)
    )

  def plot(self):
    self.fig, self.axes = plt.subplots(2, 1, height_ratios = (0.7, 0.3))

    # Set axes
    self.set_axes()

    # Initial cross-section plot
    self.tile = self.axes[0].imshow(
      self.var.value[self.time, :, :], cmap = self.cmap, vmin = self.vmin, vmax = self.vmax
    )

    # Line for water level
    self.hline = self.axes[0].axhline(y = self.model.constants["water_level"][self.time] * 100 / self.model.res)

    self.cbar = plt.colorbar(self.tile)
    self.cbar.ax.set_ylabel(self.var.name)

    # Initial line plot
    self.axes[1].plot(self.model.time, self.sum_by_time, "r--", label = self.var.name)
    self.axes[1].axvline(x = self.model.time[self.time])

    # Synchronize everything
    self.update_var(self.var.name)
    
    # Make space for slider and radio buttons
    self.fig.subplots_adjust(left = 0.3, bottom = 0.2)

    # Slider to control the time
    axtime = self.fig.add_axes([0.33, 0.1, 0.55, 0.03])
    time_slider = Slider(
        ax = axtime,
        label = 'Time (d)',
        valmin = self.model.t_0,
        valmax = self.model.t_f,
        valinit = self.model.t_0 + self.model.dt,
        valstep = self.model.dt
    )

    # Radio buttons to choose the variable
    axbuttons = self.fig.add_axes([0, 0.25, 0.2, 0.65])
    var_buttons = RadioButtons(
      axbuttons,
      labels = list(self.var_names.keys()),
      active = list(self.var_names.keys()).index(self.var.name)
    )

    time_slider.on_changed(self.update_time)
    var_buttons.on_clicked(self.update_var)

    return time_slider, var_buttons, self.fig