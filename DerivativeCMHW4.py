# Calculating Derivative
import numpy as np
import matplotlib.pyplot as plt
def g(x):
    gx = np.exp(-x)
    return gx
def t(x):
    tx = x ** (x-1)
    return tx
def dfdx(func,x):
    results = []
    xvalue = []
    for k in range(2,15,2):    
        h = 10**(-k)
        deriv = (func(x-h) - func(x)) / h
        results.append(deriv)
        xvalue.append(-k)
    plt.plot(xvalue,results)
    plt.title("Derivative Accuracy")
    plt.xlabel("10 to the power of _")
    plt.ylabel("Derivative")
    plt.show()
    return xvalue, results
#argparse section
import argparse
parser = argparse.ArgumentParser(description='Calculate the derivative of one of two functions at a given point')
parser.add_argument('function', type=str, help='The function to differentiate (g or t). g(x) = e^(-x), t(x) = x^(x-1)')
parser.add_argument('x', type=float, help='The x value at which to calculate the derivative')
args = parser.parse_args()
if args.function == 'g':
    x_values, derivatives = dfdx(g, args.x)
elif args.function == 't':
    x_values, derivatives = dfdx(t, args.x)
else:    print("Invalid function choice. Please choose 'g' or 't'.")
