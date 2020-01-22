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

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'.upper() #just to create labels

numberOfMasses = 5

dt = 0.01 #smaller values increase precision but make animation slower

totalSteps = 2000 #run for however many steps


mass = []
while(len(mass) < numberOfMasses):
    mass.append(random.randint(1,30))

velocities = []
for i in range(numberOfMasses):
     velocities.append([random.randint(-5,5) for i in range(3)])



positions = []
while(len(positions) < numberOfMasses):
    pos = [random.randint(-10,10) for i in range(3)]
    if pos not in positions:
        positions.append(pos)


velocities = np.array(velocities) #convert into a m x 3 array for each mass
positions = np.array(positions) #convert into m x 3 array of positions for each mass
accelerations = np.array([np.array([0.0,0.0,0.0]) for j in range(numberOfMasses)]) #create empty array of accelerations

def calculation(m, p, v, a, dt): #pass masses, positions and velocities arrays
    
    G = 20 #I used a custom G constant just so I can use smaller masses and smaller distance scales to make Matplotlib not freak out
    
    for i in range(numberOfMasses):
        netaccel = np.array([0.0,0.0,0.0]) #create empty array to add
        for j in range(numberOfMasses): # P[i] will change row
            
            if j != i:
                
                vec = p[j] - p[i] #find vector between masses
                distance = (math.sqrt(vec.dot(vec)))**3 #find magnitude of distance to the power of 3
                vector = ((G * mass[j]) / distance) * vec #find 1 x 3 acceleration vector
                netaccel += vector #modify net acceleration vector
                
        a[i] = netaccel #set acceleration of mass at index i to the net acceleration

    p = v * dt + 0.5 * a * dt ** 2 + p #calculate new positions
    
    v = a * dt + v #calculate new velocities

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






    
