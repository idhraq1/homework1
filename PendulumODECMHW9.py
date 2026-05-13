#This is solved very similary to our other problem, minus the animation
#We just have to use r = [theta,omega] instead of r = [x,y,vx,vy]
#Remember that the time derivative of the angular position, θ
#is the angular velocity, omega
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

#We are calculating the angle theta of displacement for several periods of the pendulum
#Variables
l = .1 #10 cm arm, length
g = 9.81 #gravity in meters per second squared
θi = np.radians(179) #initial angle given, converted to radians
omegai = 0 #our initial angular velocity, since it was released from standstill, it would be 0

h = .001 #our dt, or time step in seconds
tmax = 10 #just arbitrarily picked 10 seconds

#our time array 
tpoints = np.arange(0,tmax,h) #goes from 0 to tmax, in increments of dt

#Our two first order equations here would be θ' = omega
#and omega' = (-g/l)*sin(θ)

#So our state vector would be r = [angle, angular velocity]
r = np.array([θi,omegai]) #our state vector, with initial angle and velocity
angles = [] #list to store our angles

def deriv(r):
    θ,omega = r #unpacks our state vector into its parts
    #the deriv of theta is omega, so we dont need to do anything there
    domegadt = -(g/l) * np.sin(θ) 
    return np.array([omega,domegadt])
    
#Runge Kutta 4 Loop

for t in tpoints:
    #Since we want to solve for angles over time, we'll return the first part of the array
    angles.append(r[0]) #r[0] are our angles, we just keep adding them to the list
    #we dont need to do r.copy() here because we dont store a whole array unlike last time
    
   #Slope at the start
    k1 = h * deriv(r)
        
    #Slope halfway
    k2 = h * deriv(r + .5 * k1)
    
    #Another midpoint slope
    k3 = h * deriv(r + .5 * k2)
    
    #Slope near the end
    k4 = h * deriv(r + k3)
    
    #Average of all slopes
    r+= (k1 + 2*k2 + 2*k3 + k4) / 6

#converting list to array
angles = np.array(angles)
#plotting
def pendulumplot():
    plt.plot(tpoints,angles)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Angle (radians)")
    plt.title("Motion of Nonlinear Pendulum")
    plt.show()

def pendulumanim():
    #first we convert our angles into x and y coordinates
    x = l * np.sin(angles)
    y = -l * np.cos(angles)

    #setting up the animation
    fig,ax = plt.subplots()
    ax.set_xlim(-l,l) #setting the x limit for our animation
    ax.set_ylim(-l,l) #setting y limit. the pendulum will only go as far as the arms length, so those will be the limits

    line, = ax.plot([],[],'o-',lw=.5) #comma important here, gives us item in the list instead of the whole list
    #the empty brackets will be filled later in our update function
    #the o- just makes a line with a circle at the end

    def update(frame):
        xpos = [0,x[frame]] #this will be the x value for that frame in the animation
        ypos = [0,y[frame]] #this will be the y value for that frame

        line.set_data(xpos,ypos) #this is us drawing the line for that frame
        return line,

    #creating the animation
    ani = anim.FuncAnimation(fig,update,frames=len(x),interval=10,blit=False)
    #figure to animate, function to call each frame, number of frames, delay between frames in milliseconds, blit is just performance optimizer
        #we wanna make sure our timestep h is less than the frame rate of the anim, for more accuracy
        #our frames is = length of x because for each value of x and y, it corresponds to one timestep of the animation
        #so we want our frames to be 1:1 with our data and be in sync
    plt.xlabel("X-axis (meters)")
    plt.ylabel("Y-axis (meters)")
    plt.show()
    ani

#argparse section
import argparse

parser = argparse.ArgumentParser(description="Studying the motion of a nonlinear pendulum, plotting for angles VS time, or animating the pendulum")

parser.add_argument('function',nargs='?',type=str,default="both",help="choose: plot, anim or both")

args = parser.parse_args()

valid = {"plot", "anim", "both"}
if args.function not in valid:
    print("Invalid option. Choose: plot, anim, or both")
    exit()

if args.function in ("plot", "both"):
    pendulumplot()

if args.function in ("anim", "both"):
   pendulumanim()