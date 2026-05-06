#Assignment 7 - Fourier Transforms
#Exercise 7.1 : Fourier Transforms of Simple Functions
#Write Python programs to calculate the coefficients in the 
#discrete Fourier transforms of the following periodic functions 
#sampled at N = 1000 evenly spaced points, and make plots of their amplitudes:

#a) A single cycle of a square-wave with amplitude 1
#b) The sawtooth wave yn = n
#c) The modulated sine wave yn = sin(πn/N) sin(20πn/N)

import numpy as np
import matplotlib.pyplot as plt

N = 1000 #given number of evenly spaced points
#we need to create an array as our time (x axis)
t = np.arange(N) #goes from 0,1,2, to 999

#a) Single cycle square wave with amplitude 1
#Basically a graph looking like this _|-|_|- ...
#Stays at 1 value and suddenly switches. For example alternating between 1 and -1
#And a single cycle just means one full high+low pattern

#for our graph, we just make first 500 +1 and last 500 -1
def square():
    squarewave = np.where(t < N/2, 1, -1) #np.where(condition, value if condition is met, value if it isnt met)
    #basically just if n < 500, value is 1
    #and if n >= 500, value is -1. we use np.where because we're checking an array, if else doesnt work here
    
    #computing the fourier transform
    # a fourier transform basically turns something oscillating in terms of time
    # into in terms of frequency instead of time. 
    # this lets us turn for example a combination of multiple sounds A B C, in terms of time,
    # into in terms of frequency, where we can see the frequencies of sound to seperate and see A B C individually 
    # the formula used is function integral from -inf to inf of : f(t) * e^-j*f*t 
    # however the discrete fourier transform, which is what we use, is sum to (N-1) starting from n=0 of f(n) * e^-j*f of k*n where k goes from 0,1 to N-1
    squarefourier = np.fft.fft(squarewave) #np.fft is fast fourier transform
    
    #computing amplitude
    squareamp = np.abs(squarefourier) #since fourier transform gives complex number, abs gives magnitude so we can use it
    
    #plotting
    #time plot
    plt.figure()
    plt.plot(t, squarewave)
    plt.title("Square Wave Time")
    plt.xlabel("Time t")
    plt.ylabel("Amplitude")
    plt.show()
    plt.figure()
    #fourier plot
    plt.plot(squareamp)
    plt.title("Single Cycle Square Wave Fourier") 
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.show()
    # The graph should spike at 0, because the thing we graphed didnt really oscillate, its just a single cycle. 
    # There should also be a spike at 1000, because its just repeating the spike at 0 but negative. Since k = 0 and k = N would be the same since its periodic


#b) Sawtooth Wave yn = n
# basically a graph looking like /\/\/\/\/\ 
# however in our case, itd just look like this / since its a single cycle
# we were given yn = n, which means we just set sawtooth equal to our t array
def saw():
    sawtooth = t.copy() #makes a copy of our t array, so if anything changes in t after, this doesnt change
    
    sawfourier = np.fft.fft(sawtooth)
    
    sawamp = np.abs(sawfourier)

    #plotting
    #time graph
    plt.figure()
    plt.plot(t,sawtooth)
    plt.title("Sawtooth Wave Time")
    plt.xlabel("Time t")
    plt.ylabel("Amplitude")
    plt.show()
    #fourier graph
    plt.figure()
    plt.plot(sawamp)
    plt.title("Sawtooth Wave Fourier")
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.show()

#c) Modulated sin wave yn = sin(πn/N) sin(20πn/N)
#first just write the formula down
def modsinwave():
    modulated = np.sin(np.pi*t / N) * np.sin(20 * np.pi*t / N) #this should be a product of 2 sin waves, a slow (pin/N) and a fast (20pin/N)
    
    modfourier = np.fft.fft(modulated)
    
    modamp = np.abs(modfourier)

    #plotting
    #time graph
    plt.figure()
    plt.plot(t,modulated)
    plt.title("Modulated Sine Wave Time")
    plt.xlabel("Time t")
    plt.ylabel("Amplitude")
    plt.show()
    #fourier graph
    plt.figure()
    plt.plot(modamp)
    plt.title("Modulated Sine Wave Fourier")
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.show()
    #The fourier spikes around 10 in frequency, if you zoom in using plot(modamp[:50]).
    #argparse section
import argparse
parser = argparse.ArgumentParser(description="Fourier transforms of a Square wave, Sawtooth wave, and Modulated Sin Wave")

parser.add_argument('function',nargs='?',type=str,default="all",help="choose: square, sawtooth, modulated, or all")

args = parser.parse_args()

valid = {"square", "sawtooth", "modulated","all"}
if args.function not in valid:
    print("Invalid option. Choose: square, sawtooth, modulated, or all")
    exit()

if args.function in ("square", "all"):
    square()
if args.function in ("sawtooth", "all"):
    saw()
if args.function in("modulated","all"):
    modsinwave()
