# Physical-biological model of an estuarine ecosystem in python.

This model is made of a grid of cells, and updates each of the cells for every time-step to represent the evolution of different variables (eg. light, nutrients, phytoplankton etc.).
Each cell has a value for all of the variables of the model, and can update these values based its position and the values at time = t - 1.

For instance, here is the visualization of light availability in the estuary : light is maximal at the surface then decreases exponentially with depth. 
On the bottom, you can see total light in the system relative to time. This is a simple day/night cycle with a $sin$ wave. Note that the cross-section above only shows the model state at time = t.

![Visualization of model output](Images/Demonstration.png)

All of the equations used in the model are located in tools/equations.py. To run the model, run the file estuarine_model.py.

For now, the model only simulates a 2d cross-section of the river, but we can add the third dimension later.

**Useful resources** :
- <https://nbviewer.org/github/barbagroup/CFDPython/blob/master/lessons/01_Step_1.ipynb>