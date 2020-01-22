# N-Body-Simulator
Accurately simulates masses orbiting around each other

Built using Python 3.8.

User can create masses with an initial position and velocity, and then the net acceleration for each object is continously calculated. The position and velocity is updated with each new net acceleration calculation. A note, the acceleration is calculated using simple Newtonian vector mechanics, not differential equations. 

There are two versions: One involving four matrices (Numpy arrays): Position, Velocity, Acceleration and Mass matrices; and one involving a dictionary of the form, {mass:[Position, Velocity]}. 

It appears that the dictionary method is actually slightly faster, however, obviously doesn't allow for two of the same masses to be simulated. 

# Dependencies

- Python (Any version which supports the following dependencies will do)
- Matplotlib (Any version as long as it supports 3D plotting and animations)
- Numpy
- Math, Random, Time

