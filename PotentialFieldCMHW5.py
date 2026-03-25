#Lab Exercise - 5.21 - Differentiation : Electric Field of a Charge
#For point charge q at origin, electric potential at r from origin is 
# e.pot = q / 4pi(eps)r
# Electric field E = -gradient(e.pot)

#2 charges 1C and -1C, 10 cm apart
#Calc e.pot on 1m x 1m plane surrounding the charges and passing through them
#Calc potential at 1 cm spaced points in a grid and make visualization on the screen of potential using desnity plot
#Basically want to calc e.pot for r from 1 to 10 for each charge
import astropy.constants as cons
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt

#making the grid
potentials = np.zeros((100,100)) #making the 2d array. zeros makes it so the array is filled with 0s
def potential():
    
    for i in range (-50,50,1): #These would be our y values
        for k in range(-50,50,1): #These would be our x values
            q1 = 1
            q2 = -1
            
            x1 = -5
            x2 = 5
            
            r1s = (i-x1)**2 + (k)**2 #distance eq (x^2 + y^2 = r^2) 
            r1 = (r1s**.5)/100 #have to unit convert cm to m, using /100
            
            r2s = (i-x2)**2 + (k)**2 
            r2 = (r2s**.5)/100 #have to unit convert cm to m, using /100
            
            
            epot = (q1/(4*np.pi*cons.eps0.value*r1)) + (q2/(4*np.pi*cons.eps0.value*r2))
            
            potentials[k+50,i+50] = epot #Arrays dont like negative numbers, so we shift the entire thing by 50 to remove negatives
            
    # Need to sum both potentials at each point on the grid
    # Now to actually plot the grid
    plt.imshow(potentials, cmap = 'plasma', extent=[-.5,.5,-.5,.5]) #extent is just how big you want graph to be, since we want 1m x 1m, we go from -0.5m to 0.5m
    plt.colorbar(label="Electric Potential")
    plt.xlabel("x (meters)")
    plt.ylabel("y (meters)")
    plt.title("Electric Potential of Two Charges")
    plt.show()

#Part 2 of Exercise 5.21
#Calculate partial derivs of the potential with respect to x and y to find the electric field in the xy plane
#Remember that Electric field is = - gradient of e.potential
#Make a visualization of the electric field also

#To find the partial derivs, we already have epot values.
#We want to find the difference at one point divided by the distance. So example:
# d(epot)/dy = [ epot(x, y + change in y) - epot(x, y - change in y) ] / 2(change in y)
# Since we wanted 1 cm spacing between our grid, thatll be our dx and dy. It is just our grid spacing
#It is used in our equation, since its the total distance between points. So everything is divided by 2(dx)

dx = .01 #1cm spacing. Since dy would be the same, we just use dx 

#We only needed to calculate the potentials once, so we only needed 1 array.
#Here, we need the x deriv and y deriv, so we need 2 arrays. E is a vector
def electric_field():
    Ex = np.zeros((100,100)) #Electric field x
    Ey = np.zeros((100,100)) #Electric field y

    for i in range(1,99,1):
        for k in range(1,99,1):
            epotdx = (potentials[k+1,i] - potentials[k-1,i])/(2*dx)
            epotdy = (potentials[k,i+1] - potentials[k,i-1])/(2*dx)
            #must multiply by negative 1 for E

            Ex[k,i] = -epotdx
            Ey[k,i] = -epotdy

    # Now to actually plot the grid, we also want arrows for direction
    x = np.linspace(-0.5, 0.5, 100)
    y = np.linspace(-0.5, 0.5, 100)
    x, y = np.meshgrid(x, y) #have to make actual x and y coordinates for our graph
    E_mag = np.sqrt(Ex**2 + Ey**2)

    Ex_norm = Ex / (E_mag + 1e-12) #We remove the magnitude and only keep direction
    Ey_norm = Ey / (E_mag + 1e-12) #If we dont, the graph looks really bad
    step = 5 #used to reduce the amount of arrows so map doesnt suck
    plt.quiver(x[::step, ::step],y[::step, ::step],Ex_norm.T[::step, ::step],Ey_norm.T[::step, ::step]) #.T is used to transpose, without it my graph looked wrong, so we swap X and Y
    plt.xlabel("x (meters)")
    plt.ylabel("y (meters)")
    plt.title("Electric Field of Two Charges")
    plt.show()

#Argparse section
import argparse #want to use argparse so you can choose first graph, second graph, or both
parser = argparse.ArgumentParser(description='Calculate and visualize electric potential and electric field of two charges.')
parser.add_argument('function', type=str, help='Type p for potential, e for electric field, or nothing for both. Default is both.', default='both', nargs='?') #nargs is used to make the argument optional, so if you dont put anything, it will just do both
args = parser.parse_args()
if args.function == 'e':
    electric_field()
elif args.function == 'p':
    potential()
else:    
    potential()
    electric_field()