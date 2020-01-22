import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anim
import math
import random
import time

random.seed(1)

realism = False


np.set_printoptions(precision=5, suppress = True)

start = time.time()
dt = 0.01
totalSteps = 2000

if realism == True:
    
    #alphabet = ['earth', 'sun', 'moon']
    alphabet = ['earth', 'moon']
    
    
    massFactor = 1e10 #use 10,000kg = 1 MU
    distanceFactor = 1e10 #use 10,000m = 1 DU
    timeFactor = 100000 #use 10,000s = 1 TU

    m1 = 6e24 / massFactor #earth
    m2 = 1.989e30 / massFactor #sun
    #m2 = 2.4929e28 / massFactor
    m3 = 7.34767e22 / massFactor #moon


    dem = 384400*1000 / distanceFactor #m

    des = 147.1 * 10e6 * 1000 / distanceFactor #m
    #des = 50000 * 1000 / distanceFactor

    ve = 2.978589e11 * timeFactor / distanceFactor #m/s
    vm = 1022 * timeFactor / distanceFactor #m/s
    
    #bodies = {m1: [np.array((des,0,0)), np.array((0,ve,0))], m2 : [np.array((0,10,0)), np.array((0,0,0))], m3 : [np.array((dem + des,0,0)), np.array((0,vm + ve,0))]}
    #mass = [m1,m2,m3]
    #bodies = {m1: [np.array((des/10,0,0)), np.array((0,ve,0))], m2 : [np.array((0,10,0)), np.array((0,0,0))]}
    #mass = [m1,m2]
    
    bodies = {m1: [np.array((0,0,0)), np.array((0,0,0))], m3 : [np.array((dem,0,0)), np.array((0,vm,0))]}
    mass = [m1,m3]
    
    
else:
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'.upper()
    
    
    numberOfMasses = len(alphabet)

    mass = []
    while(len(mass) < numberOfMasses):
        m = random.randint(1,numberOfMasses)
        if m not in mass:
            mass.append(m)
    
    bodies = {}
    cbodies = {}

    #print('Adding positions and velocities to {} objects'.format(numberOfMasses))
    while(len(bodies) < numberOfMasses):
        
        p = [random.randint(-10,10) for i in range(3)]
        v = [random.randint(-5,5) for i in range(3)]
        
        if p not in list(cbodies.values()):
            for i in mass:
                if i not in list(bodies.keys()):
                    bodies[i] = [np.array(p),np.array(v)]
                    cbodies[i] = [p,v]
                    #print('Added position {} and velocity {} to mass {}'.format(p,v,i))
                    break
            
   # bodies = {m1: [np.random.randint(-10, 10, 3), np.random.randint(-10, 10, 3)], m2 : [np.random.randint(-10, 10, 3), np.random.randint(-10, 10, 3)],
              #m3: [np.random.randint(-10, 10, 3), np.random.randint(-10, 10, 3)], m4 : [np.random.randint(-10, 10, 3), np.random.randint(-10, 10, 3)]}

    

#mass = [4,1000]
#bodies = {1000:[np.array((0,0,0)),np.array((0,0,0))],4:[np.array((0,0,10)),np.array((0,32,0))]}

loc = []
vel = []

def newPos(pos, vel, accel, dt):
    return vel * dt + 0.5 * accel * dt ** 2 + pos

def newVel(vel, accel, dt):
    return accel * dt + vel

def length(vector, summ = 0):
    for i in vector: summ += i**2
    return math.sqrt(summ)


def calculation(bodies, dt): #dictionary: mass:position, velocity

    if realism == True:
        G = 6.67384e-11 * (((1/distanceFactor)**3)/(((1/massFactor)) * (1/timeFactor) ** 2))
    else:
        G = 10

    accelerations = []
    for i in bodies:
        accel = np.array([0.0,0.0,0.0])
        for j in bodies: #Calculate net acceleration on body
            if i != j:
                vectorBetween = bodies[j][0] - bodies[i][0] #find vector between
                #vectorBetween = vectorBetween.astype(np.float64)
                #vectorBetween = np.round(vectorBetween, 2)
                magBetween = math.sqrt(vectorBetween.dot(vectorBetween)) #find magnitude between
                magAccel = (G * j / magBetween**3)
                vectorAccel = (vectorBetween * magAccel)
                accel += vectorAccel #find acceleration scalar and add to previous
                #print('Vector between: {}, Distance between: {}, acceleration: {}, acceleration vector: {}, checking {} vs {}'.format(vectorBetween, magBetween, magAccel, vectorAccel, i, j))
        
        
        #print('Net Acceleration of object {} is {}'.format(i, accel))            
            
        
        accelerations.append(accel) #add net acceleration
        #accelerations = np.array(accelerations) #convert into numpy array

    for i in range(len(bodies)): #Calculate new velocity of each object
        index = list(bodies.keys())[i]
        vel = newVel(bodies[index][1], accelerations[i], dt)
        bodies[index][1] = vel
        #print('Velocity: {}'.format(vel))
    
    #print(len(bodies))
    for i in range(len(bodies)): #Calculate new positions in space
        index = list(bodies.keys())[i]
        pos = newPos(bodies[index][0], bodies[index][1], accelerations[i], dt)
        bodies[index][0] = pos
        #print(bodies)
        #print('Position: {}'.format(pos))
        

    #print('\n')
    
    

    return bodies #Return dictionary containing positions and velocities of each object



locations = {}

#print("{} masses used".format(len(mass)))

for i in mass:
    locations[i] = []

#print('{} entries added to locations variable'.format(len(locations)))

#print('Running calculations for {} steps'.format(totalSteps))

prevI = 0
for i in range(totalSteps):
    #print((i * 100) // totalSteps, i / totalSteps)
    if (i * 100) // totalSteps % 1 == 0 and (i * 100) // totalSteps != prevI :
        print('{}% done'.format(i * 100 /totalSteps))
        prevI = (i * 100) // totalSteps
    for j in locations:
        locations[j].append(bodies[j][0])
    bodies = calculation(bodies, dt)

#print('Creating Figure')

hexa = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
colours = []
for i in range(numberOfMasses):
    col = '#'
    for j in range(6):
        col += hexa[random.randint(0,15)]
    colours.append(col)


#print('Created {} colours'.format(len(colours)))

fig=plt.figure(figsize=(10,10))#Create 3D axes
ax=fig.add_subplot(111,projection="3d")#Plot the orbits
ax.autoscale()


lines = [] #total past positions
plines = [] #current position

#print('Creating {} lines'.format(len(mass)))

for i in range(len(mass)):
    a, = ax.plot([], [], [], label = 'Planet {}, Mass: {}'.format(alphabet[i], mass[i]), color = colours[i])
    lines.append(a)

#print('{} lines created'.format(len(lines)))


#print('Creating {} markers'.format(len(mass)))
for i in range(len(mass)):
    a, = ax.plot([], [], [], marker=".", color = colours[i])
    plines.append(a)

#print('{} markers created'.format(len(plines)))

#print('Creating legend')
ax.legend(lines, [i.get_label() for i in lines], loc=0)

datalines = {}
pdatalines = {}

#print('Creating {0} data dictionaries and {0} marker dictionaries'.format(len(lines)))

for j,i in enumerate(lines):
    #print(j)
    index = locations[list(locations.keys())[j]]
    datalines[i] = index #create dictionary with a list containing line data 
    pdatalines[plines[j]] = np.empty(3) #create a dictionary with current position (starts at 0,0,0)

#print('Created {} lines with data, and {} markers with data'.format(len(datalines),len(pdatalines)))

xhigh = 20
yhigh = 20
zhigh = 20

def update(num): #datalines is dictionary where key:value is line:data


    #if num * 100 // totalSteps % 10 == 0:
        #print('{}% done'.format(num * 100 /totalSteps))
    
    x = []
    y = []
    z = []

    global xhigh
    global yhigh
    global zhigh


    ax.set_xlim([-1 * xhigh,xhigh])
    ax.set_ylim([-1 * yhigh,yhigh])
    ax.set_zlim([-1 * zhigh,zhigh])
    
    if num == 0:
        num += 1
    

    for j,i in enumerate(datalines): #get line and its position
        
        index = np.array(datalines[i])
        pindex = list(pdatalines.keys())[j] #gets marker line in the same position as data line

        pindex.set_data(index[:,0][:num],index[:,1][:num])
        pindex.set_3d_properties(index[:,2][num])

        
        
        i.set_data(index[:,0][:num],index[:,1][:num])
        
        i.set_3d_properties(index[:,2][:num])

        #print(index[:,0][:num])
        
        x.append(float(index[:,0][num]))
        y.append(float(index[:,1][num]))
        z.append(float(index[:,2][num]))

    for j,i in enumerate(pdatalines):
        index = np.array(datalines[list(datalines.keys())[j]]) #take the associated line's dataset
        i.set_data(index[:,0][num],index[:,1][num])
        i.set_3d_properties(index[:,2][num])

    #print(x[0])

    if max(x) > xhigh:
        xhigh = max(x)
    if max(y) > yhigh:
        yhigh = max(y)
    if max(z) > zhigh:
        zhigh = max(z)

    


#print(type(datalines))

def animated():
    
    ani = anim.FuncAnimation(fig, update, totalSteps, interval = 1)
    #ani.save('orbits.mp4', fps=60)
    end = time.time()
    print('Simulation took {} seconds to complete'.format(end-start))
    plt.show()
    
    
    

def fakeanim():
    plt.ion()
    plt.show()
    for j in range(len(list(locations.values())[0])):
        #print(j)
        for i in locations:
            index = np.array(locations[i])
            ax.plot(index[:,0][:j],index[:,1][:j],index[:,2][:j], label = 'Planet {}'.format(alphabet[list(locations.keys()).index(i)]))
            ax.legend(lines, [i.get_label() for i in lines], loc=0)
            
            
        #print('updated!')
        plt.pause(0.00001)
        plt.cla()


def once():
    for i in locations:
        index = np.array(locations[i])
        ax.plot(index[:,0],index[:,1],index[:,2], label = 'Planet {}'.format(alphabet[list(locations.keys()).index(i)]))
        ax.legend(lines, [i.get_label() for i in lines], loc=0)
        
    plt.show()

    
if __name__ == '__main__':
    animated()


