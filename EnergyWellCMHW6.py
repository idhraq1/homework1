#Assignment 6 - Exercise 6.14
#Square Potential Well 
#In a square potential well with width w and height V,
#it can be shown that the allowed energies E of a single
#quantum particle of mass using Schroodingers equation,
#are large equations for even numbered states or another 
#equation for odd numbered states.

#For part 1, we basically just want to plot 3 quantities
# y1 = tan*sqrt(w^2 * m * E/2 * hbar^2)
# y2 = sqrt(V - E / E) 
# y3 = - sqrt(E / V - E)
#all on the same graph, as a function from E = 0 to 20eV
#Using the plot, we will predict the first 6 energy levels of the particle

import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as const
import astropy.units as u

#given variables
m = const.m_e #mass of electron
hbar = const.hbar #reduced Planck constant
w = 1 * u.nm #given width of well
V = 20 * u.eV #given height of potential

#creating arrays - we dont know the correct energies, so we just scan across a huge amount
E = np.linspace(0.001,19.999,1000) * u.eV #creates 1000 evenly spaced energy values between 0 and 20 eV
#avoiding exactly 0 and exactly 20 because of divide by 0 errors

E_J = E.to(u.J) #converting energy into joules
V_J = V.to(u.J) #needed to solve formula, since this formula expects joules

#y1
y1i = np.sqrt((w**2 * m * E_J) / (2* hbar**2)) #everything inside the tan
y1i = y1i.decompose() #this simplifies units, since tan needs unitless inside
y1 = np.tan(y1i.value) #.value removes units

#y2
y2 = np.sqrt(((V-E)/E).decompose().value) #computes, then simplifies, then removes units, then square root

#y3
y3 = -np.sqrt((E / (V-E)).decompose().value) #same thing

#Plotting the functions
def plot():
    plt.figure(figsize=(8,5)) #creating the blank figure where graphs will be
    #y1 plot
    plt.plot(E.value, y1, label="y1")
    #y2 plot
    plt.plot(E.value, y2, label="y2")
    #y3 plot
    plt.plot(E.value, y3, label="y3")
    
    plt.xlabel("Energy (eV)")
    plt.ylabel("y functions")
    plt.title("Square Well Energies")
    plt.legend()
    plt.ylim(-10,10) #needed or else the tangent function blows up to infinity, and zooms graph out too much
    plt.show()

#Points where y2 intersects y1 or y3 intersects y1 are the 6 energies we want
#Ignore intersecting the vertical y1 lines, those are tan blowing the graph up to infinity


#Part 2 - Using binary search to find the first 6 energies, within .001 eV accuracy
#Binary search is when you start with 1 low point, and 1 high point
#you then check if the function changes sign between them, which means the root (0) is there
# you then cut it half and then keep the half that contains the root, and keep repeating

#to find the roots we want, we first have to remember:
#y1 = y2 for even states, and y1 = y3 for odd states
#this can be rewritten as y1 - y2 = 0 and y1 - y3 = 0, since thats when the equation is satisfied

#defining those functions
def feven(E): #have to recompute E y1i and y1 in here for this to work
    E = E * u.eV
    E_J = E.to(u.J)

    y1i = np.sqrt((w**2 * m * E_J) / (2* hbar**2)).decompose()
    y1 = np.tan(y1i.value)

    y2 = np.sqrt(((V - E) / E).decompose().value)
    #y1 is left side of eq and y2 is right
    return float(y1 - y2) # float turns array into single number
    
def fodd(E): #same as before
    E = E * u.eV
    E_J = E.to(u.J)

    y1i = np.sqrt((w**2 * m * E_J) / (2* hbar**2)).decompose()
    y1 = np.tan(y1i.value)

    y3 = -np.sqrt((E / (V - E)).decompose().value)
    #y1 is left and y3 is right
    return float(y1 - y3)
    
#creating the binary search itself
def binarysearch(func,Elow,Ehigh,tolerance=.001):
    while(Ehigh - Elow) > tolerance: #will keep repeating until the interval is less than the .001 accuracy we want
        Emid = (Elow + Ehigh)/2 #finding the middle point
        f_low = func(Elow) #evaluating the functions at the end points
        fmid = func(Emid)
        if f_low * fmid < 0: #if sign changes between elow and emid, root must be in that half
            Ehigh = Emid #so we lower the upper range to emid
        else: #or else its in the other half
            Elow = Emid #so we raise the lower range to emid
    return(Elow + Ehigh)/2 #returns to middle point for final estimate
        
#now actually finding those energies
def solve():
    energies = [] #list to store results
    En = E.value #removing units from energies array so it can be used
    for i in range(len(En) - 1): #looping through the neighboring pairs
        E1 = En[i]
        E2 = En[i+1]
    
        #checking even solutions
        if feven(E1) * feven(E2) < 0:
            #if sign changes, root exists
            root = binarysearch(feven,E1,E2)
            #storing result
            energies.append(root)
            
        #checking odd solutions
        if fodd(E1) * fodd(E2) < 0:
            root = binarysearch(fodd,E1,E2)
            energies.append(root)
    
    #sorting energies from lowest to highest
    energies = sorted(set(energies))
    print("First 6 energy levels in eV:")
    for i in range(6):
        print(f"Level {i}: {energies[i]:.3f} ev")
    
#argparse section
import argparse

parser = argparse.ArgumentParser(description="square well solver")

parser.add_argument('function',nargs='?',type=str,default="both",help="choose: plot, solve, or both")

args = parser.parse_args()

valid = {"plot", "solve", "both"}
if args.function not in valid:
    print("Invalid option. Choose: plot, solve, or both")
    exit()

if args.function in ("plot", "both"):
    plot()

if args.function in ("solve", "both"):
    solve()