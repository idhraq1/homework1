#Assignment 8 - Monte Carlo Method
#Exercise 10.3 - Brownian Motion
#Brownian motion is the motion of a particle, such as a smoke or dust particle,
#in a gas, as it is buffeted by random collisions with gas molecules. 
#Make a simple computer simulation of such a particle in two dimensions as 
#follows. The particle is confined to a square grid or lattice L × L squares on
#a side, so that its position can be represented by two 
#integers i, j = 0 . . . L − 1. It starts in the middle of the grid.
#On each step of the simulation, choose a random direction—up, down, left, or right—
#and move the particle one step in that direction. This process is called a random walk.
#The particle is not allowed to move outside the limits of the lattice—if it tries to do so, choose a new random direction to move in.
#Write a program to perform a million steps of this process on a lattice with L = 101 and 
#make an animation on the screen of the position of the particle.
#(We choose an odd length for the side of the square so that there is one lattice site exactly in the center.)

#TLDR for this is, we make a 2D grid, and have a particle start in the middle. Then have it randomly move in
#any cardinal direction by 1 step, and repeat that a lot. This is called a random walk
#It cant leave the square grid we made, and if it tries, we make it choose another direction
#part 1
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

def parta():
    #Grid size - L x L lattice
    #Middle - (L/2,L/2) with i (x) and j (y) as our position

    L = 101 #given , means it goes from 0 to 100
    N = 10000
    #creating x and y arrays
    i = np.zeros(N+1) #uses N + 1 because the +1 is including the starting point
    j = np.zeros(N+1) #and we use N because thats the amount the particle will move

    i0 = L // 2 #initial x position , use integer divide so it doesnt become a decimal answer
    j0 = L // 2 #initial y position

    i[0] = i0 #setting the initial positions in the array
    j[0] = j0

    for k in range(1,N+1):
        direction = np.random.choice(['up','down','left','right']) #this will pick randomly between our 4 choices in the list

        if direction == 'up':
            newi = i0
            newj = j0 + 1
        elif direction == 'down':
            newi = i0
            newj = j0 - 1
        elif direction == 'left':
            newi = i0 - 1
            newj = j0 
        elif direction == 'right':
            newi = i0 + 1
            newj = j0

        if 0 <= newi < L and 0 <= newj < L: #checking if it leaves boundaries, 0 is left/bottom boundary and L is right/top
            i0 = newi #basically, if it doesnt leave the boundary, then it gets set
            j0 = newj 
        #storing the new positions
        i[k] = i0 #the kth value is replaced with the new i. if it leaves the boundary, then it just sticks with the k-1 value beforehand
        j[k] = j0 


    #setting up the animation, using plt

    fig,ax = plt.subplots(figsize=(6,6)) 

    ax.set_xlim(0,L) #setting the limits for the plot x
    ax.set_ylim(0,L) #y limit

    #creating the objects that can be updated by the animation later
    #brackets are empty because we give it the data later, in update

    line, = ax.plot([],[],lw=.5) #creating empty trail linem lw is line width
    #the comma here is very important, it basically gives us the number inside the list instead of the whole list
    #matplotlib automatically makes a list when making a plot
    #animation doesnt want a list but a an object that exists on the graph that you can change


    particle, = ax.plot([],[],'ro') #creating the particle, r is red and o means circle
    #same for the comma here

    def update(frame): #creating the function to say what the drawing looks like each frame, basically at (frame) , update the graph to look like this

        line.set_data(i[:frame], j[:frame]) #drawing trail up to current frame, comma means to take all x/y positions up to that frame

        particle.set_data([i[frame]], [j[frame]]) #draw current particle position

        return line, particle

    #creating the actual animation
    ani = anim.FuncAnimation(fig,update,frames=N,interval=1,blit=False)
    # figure to animate, function to call each frame, number of frames, delay between frames in milliseconds, blit is just performance optimizer, if you leave it on it will only redraw elements that change

    # Show animation
    plt.draw()
    plt.show()

    ani

#Part 2 - Exercise 10.8: Calculate a value for the integral

# I = integral(1-0) of ( x^(-1/2) / e^(x) + 1 ) dx,
#using the importance sampling formula, Eq. (10.42), with w(x) = x−1/2, as follows:
#a) Show that the probability distribution p(x) from which the sample points should be drawn is given by
#p(x) = 1 / 2* (x)^1/2
#and derive a transformation formula for generating random numbers between zero and one from this distribution.
#b) Using your formula, sample N = 1,000,000 random points and hence evaluate the integral. You should get a value around 0.84.

#TLDR for this is, we're trying to approximate integral I using Monte Carlo method
#Our given weight function is w(x) = x^-1/2 , and 
#we're trying to derive the probability density is the p(x) given, as well as a formula for generating random numbers from that distribution for part a

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

#Part a - in importance sampling, p(x) = w(x)/integral of w(x)dx from a to b

# The idea is that we want to compute the integral I, but x^-1/2 gets very large near x = 0
# So normal Monte Carlo method has trouble working properly.
# So instead, they choose a weight function w(x) = x^-1/2, because this is the "bad" part of the integral
# If they sample points in the same shape as the divergence, the divergence cancels

#They make a new function g(x), which is just f(x) with the bad part removed, or f(x)/w(x)
#g(x) = 1/e^x + 1

# They then convert w(x) into a probability distribution
# So our p(x) = x^-1/2 / integral from 0 - 1 (since probability goes up to 1) of x^-1/2, which would solve into 1/2*x^1/2, and thats what we were given
# This is the distribution we want to sample from


# The transformation formula is for turning ordinary uniform random numbers into numbers distributed like p(x)
# We dont want uniform points anymore, we want points distributed like p(x), so we want a way to turn uniform random numbers into this

#To get the transformation formula, we get the CDF
# P(x) = integral of our p(t)dt function from 0 to x. (we replace x with t in p(x))
# Plugging in our 1/(2(t)^1/2), we basically just integrate it to get P(x) = (x)^1/2

# A uniform random number u, would satify u = P(x), so u = (x)^1/2
# And when you solve for x, you get x = u^2. This would be our transformation formula

#To wrap it all up, for part b, we're gonna get N amount of uniform random numbers, u,
#and then we transform them to our x values which are distributed using p(x)
#then, we use our g(x) formula, which uses our x, and take the mean of it (finding the average, 1/N * sum of our formula to N)
#as well as multiply it with the integral(0 to 1) of our w(x) function
#since w(x) = x^-1/2, the integral of x^-1/2 going from 0 to 1 is 2 * x^1/2, where x is replaced with 1, so 2


#Part b - evaluate integral using sample N = 1mil, should be around .84
def partb():
    N = 1000000 #1 mil
    u = np.random.random(N) # our N uniform random numbers, that we are gonna transform
    x = u**2 # our transformation formula, now x values are distributed using p(x)

    # our g(x)
    g = 1/ (np.exp(x) + 1)

    # the mean of our g function, times the integral of our w(x) function, which is 2
    I = np.mean(g) * 2 #this will give us our evaluated value of the integral
    return(I)
    #we get almost .84, which lines up

#argparse section
import argparse

parser = argparse.ArgumentParser(description="Monte Carlo Method - Brownian animation or integral solver")

parser.add_argument('function',nargs='?',type=str,default="both",help="choose: anim, integral or both")

args = parser.parse_args()

valid = {"anim", "integral", "both"}
if args.function not in valid:
    print("Invalid option. Choose: anim, integral, or both")
    exit()

if args.function in ("anim", "both"):
    parta()

if args.function in ("integral", "both"):
   I = partb()
   print(f"Estimated integral: {I:.3f}") #the first f is formatting, lets me write variables inside the " ".
   #the :.3f just makes it so the answer is reduced to the first 3 decimals 