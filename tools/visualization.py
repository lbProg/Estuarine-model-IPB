import matplotlib.pyplot as plt

from classes.plot import Plot

# Cross-section plot to show a slice of the model through time

def plot(initial_var, model) :
  cross_plot = Plot(initial_var, model)
  return cross_plot.plot()

def visualize_results(models):
  sliders = [0] * len(models)
  buttons = [0] * len(models)
  figs = [0] * len(models)
  for i in range(len(models)):
    sliders[i], buttons[i], figs[i] = models[i].plot_results(list(models[i].variables)[0])

  plt.show()