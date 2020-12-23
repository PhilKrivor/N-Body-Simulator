import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anim
import math
import random
import time

#random.seed(1)
np.set_printoptions(precision=5, suppress=True)

start = time.time()

random_test = True #boolean for testing random planets on a smaller scale vs. realistic simulations

choice = 3

# sqrt(300 * 5 / 8)

if choice == 1:
    numberOfMasses = 2
    alphabet = [i for i in range(numberOfMasses)]

    dt = 0.1 #smaller values increase precision but make animation slower

    totalSteps = 2000 #run for however many steps

    mass = [300, 0.1]
    positions = [[0,0,0],[0,10,0]]
    velocities = [[0,0,0],[(300 * 5 / 10)**0.5,0,0]]


elif choice == 3:

    #alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'.upper() #just to create labels
    

    numberOfMasses = 5
    alphabet = [i for i in range(numberOfMasses)]

    dt = 1 #smaller values increase precision but make animation slower

    totalSteps = 2000 #run for however many steps


    mass = []
    while(len(mass) < numberOfMasses):
        mass.append(random.randint(1,30))

    #velocities = [[0,0,0],[(1500/8)**0.5,0,0]]
    #velocities = [[0,0,0], [‭0,0,0]]
    #velocities = [[0,0,0], [‭]]
    velocities = []
    for i in range(numberOfMasses):
         velocities.append([random.randint(-5,5) for i in range(3)])



    #positions = [[0,0,0], [0, 8, 0]]
    positions = []
    while(len(positions) < numberOfMasses):
        pos = [random.randint(-10,10) for i in range(3)]
        if pos not in positions:
            positions.append(pos)
elif choice == 2:

    print('Starting realistic simulation...')

    dt = 10
    totalSteps = 2000
    numberOfMasses = 3

    alphabet = ['Earth', 'Sun', 'Moon']

    massFactor = 1e20 #use 1e20 kg = 1 MU
    distanceFactor = 1e5 #use 10,000m = 1 DU
    timeFactor = 100000 #use 10,000s = 1 TU
    G = 6.67384e-11 * (((1/distanceFactor)**3)/(((1/massFactor)) * (1/timeFactor) ** 2))

    mass_earth = 6e24 / massFactor
    mass_sun = 1.989e30 / massFactor
    mass_moon = 7.34767e22 / massFactor

    distance_earth_to_moon = 324400*1000 / distanceFactor
    distance_earth_to_sun = 147.1 * 10e6 * 1000 / distanceFactor

    #velocity_earth = 2.978589e4 * timeFactor / distanceFactor
    #velocity_earth = 5e3 * timeFactor / distanceFactor
    #velocity_moon = 5.1e3 * timeFactor / distanceFactor
    velocity_earth = (mass_sun * G / distance_earth_to_sun)**0.5
    velocity_moon = (mass_earth * G / distance_earth_to_moon)**0.5 + velocity_earth

    mass = [mass_earth, mass_sun, mass_moon]
    velocities = [[velocity_earth, 0, 0], [0,0,0], [velocity_moon, 0, 0]]
    positions = [[0, distance_earth_to_sun, 0], [0,0,0], [0, distance_earth_to_sun + distance_earth_to_moon, 0]]
    


velocities = np.array(velocities) #convert into a m x 3 array for each mass
positions = np.array(positions) #convert into m x 3 array of positions for each mass
accelerations = np.array([np.array([0.0,0.0,0.0]) for j in range(numberOfMasses)]) #create empty array of accelerations
mass = np.array(mass)
mass = np.reshape(mass, (1, mass.shape[0])).T
#velocities = np.reshape(velocities, (1, velocities.shape[0]))
#positions = np.reshape(positions, (1, positions.shape[0]))

def calculation(m, p, v, a, dt): #pass masses, positions and velocities arrays

    if random_test:
        G = 5 #I used a custom G constant just so I can use smaller masses and smaller distance scales to make Matplotlib not freak out
    else:
        G = 6.67384e-11 * (((1/distanceFactor)**3)/(((1/massFactor)) * (1/timeFactor) ** 2))
    
    for i in range(numberOfMasses):

        
        other_masses = np.vstack((m[0:i, :],m[i+1:, :]))
    
        
        others = np.vstack((p[0:i, :],p[i+1:, :]))
    
        target = p[i, :]
        
        vec_between = others - target

       

        distance = np.diagonal(np.dot(vec_between, vec_between.T))

       

        r_norm = G / ((distance)**(3/2))

       

        term = np.multiply(other_masses.T, r_norm.T).T 

        acceleration = np.multiply(vec_between.T, term.T).T

        acceleration = (1/2) * (acceleration + np.multiply(vec_between.T, term.T).T)

        netaccel = np.sum(acceleration, axis=0)

        
        a[i] = netaccel #set acceleration of mass at index i to the net acceleration


    v = a * dt/2 + v #calculate new velocities

    p = v * dt + 0.5 * a * dt ** 2 + p #calculate new positions
    
    v = a * dt/2 + v #calculate new velocities

    return p, v, a

locations = [] #create a list of position matrices
prevI = 0 #only used to print out percentage calculations done


percentage = 10 #change how much progress you see
for i in range(totalSteps):
    if (i * 100) // totalSteps % percentage == 0 and (i * 100) // totalSteps != prevI :
        print('{}% done'.format(i * 100 /totalSteps))
        prevI = (i * 100) // totalSteps

    
    positions, velocities, accelerations = calculation(mass, positions, velocities, accelerations, dt)
    
    locations.append(positions) #Yes I can use np.concatenate(), but I didn't realize I needed a tuple as the first argument for a long time, so I did a workaround :)

locs = np.array(locations) #Convert to numpy array

print(f'Time taken: {time.time() - start}')
 
print('Creating Figure')

hexa = '0123456789ABCDEF' 
colours = []
for i in range(numberOfMasses): #create a random list of colours to draw lines
    col = '#'
    for j in range(6):
        col += hexa[random.randint(0,15)]
    colours.append(col)

print('Created {} colours'.format(len(colours)))

fig=plt.figure(figsize=(10,10))#Create 3D axes
ax=fig.add_subplot(111,projection="3d")#Plot the orbits
ax.autoscale() #Scale axis

lines = [] #total past positions
plines = [] #current position (for dot)

print('Creating {} lines'.format(len(mass)))

for i in range(len(mass)): #create each line with a label containing its ID and mass, with a colour
    a, = ax.plot([], [], [], label = 'Planet {}, Mass: {}'.format(alphabet[i], mass[i]), color = colours[i])
    lines.append(a) 

print('{} lines created'.format(len(lines)))
print('Creating {} markers'.format(len(mass)))

for i in range(len(mass)): #create a dot "line" to basically act as a visual aid to the current mass location in space, has the same colour as the line it's associated with
    a, = ax.plot([], [], [], marker=".", color = colours[i])
    plines.append(a)

plines = np.array(plines)

print('{} markers created'.format(len(plines)))

print('Creating legend')
ax.legend(lines, [i.get_label() for i in lines], loc=0) #Creates legend

datalines = {} #create dictionaries with lines as keys. Theoretically, there shouldn't be any identical lines. 
pdatalines = {}

print('Creating {0} data dictionaries and {0} marker dictionaries'.format(len(lines)))

for j,i in enumerate(lines):
    index = [i[j] for i in locations] # for each element, take jth row, and append to list
    datalines[i] = index #create dictionary with a list containing line data 
    pdatalines[plines[j]] = np.empty(3) #create a dictionary with current position (starts at 0,0,0)

print('Created {} lines with data, and {} markers with data'.format(len(datalines),len(pdatalines)))

xhigh = 20 #set reasonable initial highest axis values
yhigh = 20
zhigh = 20



def update2(num):
    pass

def update(num): #datalines is dictionary where key:value is line:data
    
    x = []
    y = []
    z = []
    
    if num == 0:
        num += 1
    
    for j,i in enumerate(datalines): #get line and its position

        # locations is list of matrices with m x 3 size
        
        index = np.array(datalines[i])

        
        #print(index[:num].size)
        #pindex = list(pdatalines.keys())[j] #gets marker line in the same position as data line

        #pindex.set_data(index[:num][:,0],index[:num][:,1])
        #pindex.set_3d_properties(index[:num][:,2])

        
        i.set_data(index[:num][:,0],index[:num][:,1]) #update each line to include new and past data
        
        i.set_3d_properties(index[:num][:,2])
        
        x.append(float(index[:,0][num]))
        y.append(float(index[:,1][num]))
        z.append(float(index[:,2][num]))

    for j,i in enumerate(pdatalines):
        index = np.array(datalines[list(datalines.keys())[j]]) #take the associated line's dataset
        i.set_data(index[:,0][num],index[:,1][num]) #update marker's position to current mass position (ie most recent coordinates)
        i.set_3d_properties(index[:,2][num])

    global xhigh #declare global variables to maintain the current axis scale between animation iterations
    global yhigh
    global zhigh
    
    #Logic for finding the highest data point for each axis to adjust axis
    if max(x) > -min(x):
        if max(x) > xhigh:
            xhigh = max(x)
    elif -min(x) > max(x):
        if -min(x) > xhigh:
            xhigh = -min(x)

    if max(y) > -min(y):
        if max(y) > yhigh:
            yhigh = max(y)
    elif -min(y) > max(y):
        if -min(y) > yhigh:
            yhigh = -min(y)

    if max(z) > -min(z):
        if max(z) > zhigh:
            zhigh = max(z)
    elif -min(z) > max(z):
        if -min(z) > zhigh:
            zhigh = -min(z)

    ax.set_xlim([-1 * xhigh,xhigh]) #adjusts axis
    ax.set_ylim([-1 * yhigh,yhigh])
    ax.set_zlim([-1 * zhigh,zhigh])

def animated():
    
    ani = anim.FuncAnimation(fig, update, totalSteps, interval = 1)
    #ani.save('orbits.mp4', fps=60)
    end = time.time()
    print('Simulation took {} seconds to complete'.format(end-start))
    plt.show()
    
    
if __name__ == '__main__':
    animated()






    
