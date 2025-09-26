Physical-biological model of an estuarine ecosystem in python.

This model is made of a grid of cells, and updates each of the cells for every time-step to represent the evolution of different variables (eg. light, nutrients, phytoplankton etc.).
Each cell has a value for all of the variables of the model, and can update these values based on the values of the variables at t-1 for itself or the neighbouring cells.

![](Images/Demonstration.png)