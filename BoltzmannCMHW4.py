import astropy.constants as cons #Astropy already has all physics constants listed, we just have to use astropy.(whatever we want)
import astropy.units as u #same for units
import numpy as np

W0 = (cons.k_B**4) / (4*np.pi**2 * cons.c**2 * cons.hbar**3) #use this for part c
def f(x):
    if x == 0:
        return 0
    return (x**3) / (np.exp(x) - 1 )

#Solve integral using trapezoid method from last class  (this one wont, have to do inf integral version) 
def IntTrap(f,Nmax,a,b):
    k = 1
    h = ((b-a)/Nmax)
    SumPoints = 0
    while (k<Nmax):
        SumPoints = SumPoints + f(a + k*h)
        k = k+1
    F = h *((f(a)/2) + (f(b)/2) + SumPoints)
    return F

def Inf(z): #replacing x in our function with function z/1-z. If z = 0, then x = 0, and if z = 1, then x is infinity (Divided by 0))
    x = z/(1-z)
    return f(x)/(1-z)**2

def IntTrapInfinity(Nmax):
    eps = 1e-10 #If we let our max equal 1, we will get divide by 0 error. So we use eps to make it not exactly 1, just subtracting it by a small number
    return IntTrap(Inf,Nmax,0,1-eps)
result = IntTrapInfinity(1000)


#Check value  for Stefan Boltzmann constant
o  = W0 * result

import argparse
parser = argparse.ArgumentParser(description='Calculate the integral of x^3/(e^x - 1) from 0 to infinity using the trapezoidal method.')
parser.add_argument('--Nmax', type=int, default=1000, help='Number of subdivisions for the trapezoidal method (default: 1000)')
args = parser.parse_args()
result = IntTrapInfinity(args.Nmax)
print("The value of the integral is: ", result)
o = W0 * result
print("Our calculated Stefan-Boltzmann constant: {:.3g}".format(o))
print("The actual value of the Stefan-Boltzmann constant: {:.3g}".format(cons.sigma_sb))