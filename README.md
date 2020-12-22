# N-Body-Simulator
Accurately simulates masses orbiting around each other

Built using Python 3.8.

User can create masses with an initial position and velocity, and then the net acceleration for each object is continously calculated. The position and velocity is updated with each new net acceleration calculation. A note, the acceleration is calculated using simple Newtonian vector mechanics, not differential equations. 

There are two versions: One involving four matrices (Numpy arrays): Position, Velocity, Acceleration and Mass matrices; and one involving a dictionary of the form, {mass:[Position, Velocity]}. 

<strike>It appears that the dictionary method is actually slightly faster, however, obviously doesn't allow for two of the same masses to be simulated. </strike>

As of December 2020, the dictionary method is obsolete, and has been replaced by the newer vector version. There may be some performance to be gained in the vector version, however.

# Dependencies

- Python (Any version which supports the following dependencies will do)
- Matplotlib (Any version as long as it supports 3D plotting and animations)
- Numpy
- Math, Random, Time

# Work In Progress

I am working on implementing two kinds of pseudo-collision systems. One where two objects stick (have masses combine) and fly off, and one where the two masses annihilate each other (ie animation would stop showing two masses that collided). 

Personally, I think the sticking collision is much more interesting. 
