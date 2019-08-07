# Data  
The data here was collected using the [Current Simulation](https://github.com/joey-kilgore/Nerve-Block-Modeling/tree/master/Current%20Simulation). Most data sets have some sort of explanation in the form of a setup.txt file that should explain how you could recreate the data set should you want.  

## How is the data stored  
There are two main forms of data storage in this repo. The simplest being the direct gate values, and current values saved at every time step. This allows data analysts to see what was happening in the model, and conjecture what mechanism is causing the phenomenon being observed. The [Test AP](https://github.com/joey-kilgore/Nerve-Block-Modeling/tree/master/Data/Test%20AP) data is a good example of this. The other method for data storage takes the form of excel spreadsheets. These are used for expirements where there were numerous simulations, and saving every time step was not the goal/practical, but rather trying to quantifying a phenomena was important. The [MRG vs Freq-Dep-MRG](https://github.com/joey-kilgore/Nerve-Block-Modeling/tree/master/Data/MRG%20vs%20Freq-Dep-MRG) data is a good example of this, and was used in creating the [Frequency Dependent Membrane Capacitance Wiki](https://github.com/joey-kilgore/Nerve-Block-Modeling/wiki/Frequency-Dependent-Membrane-Capacitance)  

## **Warning**  
Some of the data might have been generated with an older version of this repository in which case it may not be recreatable with the current code. The main culprit for this was the [asymmetry bug](https://github.com/joey-kilgore/Nerve-Block-Modeling/issues/17). If you have any questions please use the [Issues](https://github.com/joey-kilgore/Nerve-Block-Modeling/issues) page and create a new issue.  