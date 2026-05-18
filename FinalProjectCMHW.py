#Pseudocode:
    #1. Using Newtons Law of Universal Gravitation, we calculate the attractive force 
    #between the black hole and the planet
        #Formula: F = (-GMm/r^2 ) * r unit vector (force pointing toward black hole)
        # unit vectors are equal to vector / magnitude, so the unit vector is (x,y) / r
        # Subbing it in F = -GMm/r^2 * (x,y)/r 
        # or have F = -GMm/r^3 * (x,y)
    #2. I wanna convert that force into acceleration using F=ma and split it into x and  y components
    #3. I also wanna set initial conditions for each one of my planets, 
        #their x and y positions, velocity, mass and timestep
    #4. For each timestep, I wanna get the distance from the planet to the blackhole
        #then use Runge Kutta 4 loop compute the accel from that position,
        # then to update the velocity using the accel and update position using velocity
    #5. Ill store every position for each planet and then use that stored position
        #to animate that orbit and use Fourier Transform to see the orbital frequencies

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
#we dont bother using astropy cause our units are our own here
#using custom units makes the simulation just easier to scale and look at, using real units could make things super large or hard to show
#the point is we're only interested in the relative motion and shape of the orbits, so scaled units doesnt change the physics

#Constants for Newtons law of UG
G = 1 #set G to 1 instead of its standard value so the simulation is stable and easier to compute
#M = 10  mass of the black hole, commented out cause i want user to input mass
dt = .01 #my timestep
tmax = 50 #simulation time
def findorbits(M):
   
    #Solving Newtons Law of UG for acceleration, using F = ma, its:
        # ax = -G * M * x / dist**3
        # ay = -G * M * y / dist**3 
        # Acceleration pulls the x and y coordinates towards 0, or our black hole

    #Each state vector here stores [x,y,vx,vy] 
    # The numbers ive put here are just the initial conditions ive decided on. Different starting radii and velocities
    states = [np.array([1,0,0,1.2]), np.array([1.5,0,0,.9]), np.array([2,0,0,.7])] #the state vectors of each planet
    tpoints = np.arange(0,tmax,dt) #the time array 
    
    trajectories = [ [],[],[] ] #lists to store the trajectory of the orbit, we have 3 planet trajectories to store
    
    #I want to turn our 2nd order equation of acceleration into 4 first order equations
    #the entire system is described by position and velocity, in x and y
    def deriv(r):
        x,y,vx,vy = r #unpacking the state vector
    
        dist = np.sqrt(x**2 + y**2) #distance from the black hole, just distance formula
    
        #gravitational acceleration
        ax = -G * M * x / dist**3
        ay = -G * M * y / dist**3 
    
        #a is 2nd deriv of position, and we basically have deriv of state depends on current state, which is good for ODEs like Runge Kutta
    
        #returning the time derivatives dx/dt, dy/dt, dvx/dt, dvy/dt
        return np.array( [vx,vy,ax,ay] )
    
    #Runge Kutta 4 loop
    for t in tpoints:
        #looping over each planet
        for i in range(len(states)):
            
            r = states[i] #current planet state vector , goes down list of arrays

            trajectories[i].append(r.copy()) #stores current state into correct trajectory
            #i use a copy so each saved row is independent 
        
            #if particle falls too close to blackhole, stop
            if np.sqrt(r[0]**2 + r[1]**2) < .05: #distance falls below .05, our event horizon
                trajectories[i].append(r.copy())
                continue
            #slope at start
            k1 = dt * deriv(r)
            #slope at midpoint
            k2 = dt * deriv(r + .5 * k1)
            #slope at midpoint using k2
            k3 = dt * deriv(r + .5 * k2)
            #slope at the end
            k4 = dt * deriv(r+k3) 
            #update r using weighted average of all slopes
            states[i] += (k1 + 2*k2 + 2*k3 + k4) / 6
        
     #converting trajectories into arrays so its better to work with
    trajectories = [ np.array(traj) for traj in trajectories ]

    return trajectories


#trajectories[0] would be planet 1 data, [1] is 2 and [2] is 3

#Now I want to animate each planets position frame by frame over time

def animateorbits(trajectories):
    #setting up the animation
    fig, ax = plt.subplots(figsize=(7,7)) #creates figure and axis
    #used figsize cause default looked small
    ax.set_aspect('equal') #use this or circles look stretched

    ax.scatter(0,0,color='black',s=150,label='Black Hole (M)') #plotting the black hole at the origin

    # draw event horizon as a circle
    event_horizon = plt.Circle((0, 0),0.05,color='purple',alpha=0.4,label='Event Horizon')

    # add circle to plot
    ax.add_patch(event_horizon)

    #plot limits
    ax.set_xlim(-2.5,2.5)
    ax.set_ylim(-2.5,2.5)

    #colors for each planet
    colors = ['red', 'blue', 'green'] 

    #creating empty line objects , the things matplotlib updates every frame, our trails
    lines = []

    for i in range(len(trajectories)): #does this 3 times
        line, = ax.plot([],[], color=colors[i],label=f'Planet {i+1}') #empty line for orbit path
        lines.append(line)

    #uses shortest trajectory length just in case 
    frames = min(len(traj) for traj in trajectories)  #traj is a temporary variable thats equal to trajectories[i]

    def init(): #initialization function, what should the animation look like before frame 0
    #clears the trails so animation begins empty
        for line in lines:

            # starts with empty data so nothing is drawn yet
            line.set_data([], [])

        return lines

    #update function, this is what draws the animation every frame
    def update(frame):
        # enumerate lets us loop through both:
        # i = index number of planet
        # traj = actual trajectory data for that planet
        #looping over each planet
        for i,traj in enumerate(trajectories):
            x = traj[:frame,0] #x values up to current frame
            y = traj[:frame,1] #y values up to current frame
            lines[i].set_data(x,y)
        return lines

    ani = anim.FuncAnimation(fig,update,frames=frames,init_func=init,interval=20,blit=True)
    #figure object, function called every frame, total # of frames, initialization func, milliseconds between frames, only redraw changing objects
    ax.set_xlabel("x position (simulated units)")
    ax.set_ylabel("y position (simulated units)")
    ax.legend() 
    plt.show()
    return ani

#Now for fourier transforms, to turn our function in terms of time to in terms of frequency

def fourier(trajectories,dt):
    #for each planet we have traj[:,0] (x[t]) and traj[:,1] (y[t]) 
    #fast fourier transforms work best with a 1 dimensional signal, so we convert to
    #r(t) = sqr( x[t]^2 + y[t]^2 ) vector to use

    #this is gonna convert motion to r(t), apply FFT, then plot the frequency spectrum

    numplanets = len(trajectories) #number of planets, we got 3

    fig,ax = plt.subplots(figsize=(6,8)) #creating figure

    colors = ['red','blue','green'] #colors for each of our planets graph

    #looping over each planet
    for i, traj in enumerate(trajectories):
        x = traj[:,0] #x(t)
        y = traj[:,1] #y(t)

        #computing r(t) radial distance
        r = np.sqrt(x**2 + y**2)
        r = r - np.mean(r) # this is suppose to improve FFT clarity by removng DC offset

        #Fast Fourier Transform
        fft_values = np.fft.fft(r) #transfrom time to frequency domain

        freqs = np.fft.fftfreq(len(r),d=dt) #corresponding frequencies

        #taking only positive frequencies (physical part)
        mask = freqs > 0
        freqs = freqs[mask]
        fft_values = np.abs(fft_values[mask]) / len(r)

        #plotting frequency all on same graph
        ax.plot(freqs, fft_values, color=colors[i],label=f'Planet{i+1}')

         #Amplitude: How much of that frequency is present, or shows which
        #orbital period dominate the motion of each planet
    ax.set_title("Orbital Frequency Spectrum (All Planets)")
    ax.set_xlabel("Frequency (1 / time unit)")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.3) #makes it look better
    ax.set_yscale('log') #makes peaks easier to see
    ax.legend()
    plt.tight_layout() #just to make it look better
    plt.show() #showing plots
    #Higher peak position = faster orbit, closer to black hole
    #lower peak is planet farther away
    #Multiple peaks = elliptical or non uniform orbit

#argparse section
import argparse

parser = argparse.ArgumentParser(description="Simulation of orbiting a Black hole, with animation and fourier analysis")

parser.add_argument('function',nargs='?',type=str,default="both",help="choose anim for animation, fourier for graphs, both for both. default is both")

parser.add_argument("--M",type=float,default=10,help="Mass of the black hole, default is 10. Not in any standard units") #lets user choose M when running in terminal
#to use it, do pythonfile.py both --M 50 for example
args = parser.parse_args()

valid = {"anim", "fourier", "both"}
if args.function not in valid:
    print("Invalid option. Choose: anim, fourier, or both")
    exit()
#running the simulation
trajectories = findorbits(args.M)

if args.function in ("anim", "both"):
    animateorbits(trajectories)

if args.function in ("fourier", "both"):
   fourier(trajectories,dt)