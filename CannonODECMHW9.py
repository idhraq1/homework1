#Showing the equations of motion for the cannon ball
# Using Newtons second law, F = ma or F = mx'' ('' is 2nd time deriv)

    # The only force in the X direction is the drag force, and drag force would be
    # going opposite against x. Same with y, but y also has gravity, which gets added onto the drag force. 
    # Since we're only given the magnitude of the drag force F, we need to give it a direction.
    # The direction would be the unit vector opposite of v. To get unit vector, its 
    # v(x/y component) / v (magnitude) , and since its opposite we attach a - sign to the whole thing
    
    # So our given F = mx'', or ((1/2) * pi * R^2 * ρ * C * v^2) * -vx/v = mx'' in the x direction, 
    # and -g - ((1/2) * pi * R^2 * ρ * C * v^2) * vy/v = my'' (adding gravity, and since they both go opposite, its -g - F)
    
    # magnitude is also just sqrt(vx^2 + vy^2) , so replace v with that and simplify the equations a bit, solving for accel
    
    # F = mx'', or -[(1/2m) * pi * R^2 * ρ * C * sqrt(vx^2 + vy^2) * vx] = x''
    # -g - [(1/2m) * pi * R^2 * ρ * C * sqrt(vx^2 + vy^2) * vy] = y''

#these are the exact same as the equations we were shown. vx is dx/dt and vy is dy/dt

#Now to turn these into 4 first order equations
    # first lets turn -[(1/2m) * pi * R^2 * ρ * C] = k, so its easier to read
    # so our equations would be x'' = -k(sqrt(vx^2 + vy^2) * vx) 
    # and y'' = -g - k(sqrt(vx^2 + vy^2) * vy)

    # y' = vy (velocity is equal to deriv of position)
    # x' = vx
    # vx' = -k(sqrt(vx^2 + vy^2) * vy) or ax  [accel is equal to deriv of velocity]
    # vy' = -g - k(sqrt(vx^2 + vy^2) * vx) or ay
#these would be our 4 first order equations

#Actual coding
import numpy as np
import matplotlib.pyplot as plt
# i dont really bother using astropy here since units here arent very complex
# We'll use Runge Kutta 4 here, as for most problems that require an ODE

#Variables, given by problem
#m = 1 #kg  - we change m later in the problem, so this is legacy
R = .08 #8cm or .08 meters
ρ = 1.22 #air density kg m^−3
C = .47 #coeffecient of drag for a sphere
g = 9.81 #meters per second squared
vi = 100 #given initial velocity, meters per second 
theta = np.radians(30) #given angle 30 degrees, converted to radians
h = .01 #our dt, or time step in seconds
tmax = 50 #just arbitrarily picked 50 seconds

def findtrajectory(m): #must input your mass in kg
    k = (np.pi * R**2 * ρ * C) / (2 * m) #our k written from before, basically just makes equation easier to read
    vxi = vi * np.cos(theta) #getting x component of our initial velocity
    vyi = vi * np.sin(theta) #getting the y component
    
    
    #array for time
    tpoints = np.arange(0,tmax,h) #goes from 0 to tmax, in increments of dt
    
    #basically storing the entire state of the cannonball in a single array
    r = np.array([0,0,vxi,vyi]) #r is just a vector storing the objects position, and velocity all in one array
    #our initial x and y positions are 0,0 , and our initial velocities are there too
    #ODEs work best using systems like dr/dt = f(r,t) [the derv of the state depends on the current state]
    
    trajectory = [] #we want to remember every position the projectile is in so we can plot the trajectory
    #at each timestep, it will store x, y ,vx ,vy inside this list
    #this uses list instead of array because we dont know how many timesteps itll take before the ball hits the ground, and arrays arent good for lists with changing max's 
    
    def deriv(r):
        x,y,vx,vy = r #basically unpacks our r vector
        v = np.sqrt(vx**2 + vy**2) #this would be the magnitude of our velocity
    
        ax = -k * vx * v #the accel equations we solved earlier
        ay = -g - k * vy * v 
    
        return np.array([vx,vy,ax,ay]) #this is basically returning dr/dt
        #or [dx/dt,dy/dt,dvx/dt,dvy/dt] or [x',y',x'',y'']
    
    #Runge Kutta 4 Loop
        # What Runge Kutta 4 does is estimate the slope 4 times, then averages them for accuracy
        # Each k is a vector and has dx dy dvx and dvy, so all variables get updated together
        # This code works for basically everything you want to use runge kutta 4 for
        # All youd have to change is the r (state vector)
        # For example, if we doing a pendulum insted, we'd just have r = [theta,omega] and do the same thing
        # We just need to find the variables that fully describe the system, and this code will work with barely any changes
        
    for t in tpoints: 
        trajectory.append(r.copy()) #saves the current state of our position and velocities into the trajectory list
        #uses copy so each saved row is independent 
    
        if r[1] < 0: #in our r vector, y is the 2nd value. this basically checks the 2nd value y, and if its less than 0 (aka hit the ground), it stops the loop
            break #stops the loop
            
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

    trajectory = np.array(trajectory) #converts the list into an array, so its easier to plot
    x = trajectory[:,0] #: means taking the entire column, and the 0 means the first part of our array, which is the x values. So it basically takes all the x values
    y = trajectory[:,1] #this takes all the y values
    
    return x,y,x[-1] #the function will return our position with all our x values, all our y values
    #it will also return the horizontal distance traveled, x[-1]. x[-1] just means the final value of our x list, which would be our horizontal range

#Plotting the trajectory
def plottrajectory(m):
    x,y,_ = findtrajectory(m) #sets our x and y as the first 2 values returned, and ignores the 3rd value returned (the x[-1])
    plt.plot(x,y) 
    plt.xlabel("x (meters)")
    plt.ylabel("y (meters)")
    plt.title("Projectile Motion with Air Resistance Trajectory")
    plt.show()

#The assignment also asks us to use different masses and see how the horizontal distance traveled changes
# We'll see the difference by plotting a mass vs range graph, and use a bunch of masses
def plotmassvsrange():
    masses = np.linspace(1,10,50) #we just make an array of masses going from 1 to 10kg, in 50 increments
    ranges = [] #we make a list to store our ranges we'd get from using those masses to calculate

    for m in masses: #goes down the mass list
        _,_,dist = findtrajectory(m) #ignores the first two values return (the x and y) and sets dist = our x[-1] returned
        ranges.append(dist) #adds that distance to the list
    plt.plot(ranges,masses)
    plt.xlabel("Range (meters)")
    plt.ylabel("Mass (kg)") 
    plt.title("Projectile Mass vs Range")
    plt.show() #from the graph shown , it shows our range increases with the mass 

#argparse section
import argparse

parser = argparse.ArgumentParser(description="Find the trajectory of a cannonball, plotting its trajectory, or plotting the mass vs range")

parser.add_argument('function',nargs='?',type=str,default="both",help="choose: trajectory, masses or both")

args = parser.parse_args()

valid = {"trajectory", "masses", "both"}
if args.function not in valid:
    print("Invalid option. Choose: trajectory, masses, or both")
    exit()

if args.function in ("trajectory", "both"):
    plottrajectory(1)

if args.function in ("masses", "both"):
   plotmassvsrange()