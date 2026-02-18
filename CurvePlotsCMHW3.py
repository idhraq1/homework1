#Comp Methods Lab
import numpy as np
import matplotlib.pyplot as plt
import argparse


#Want to use argparse to have the options of showing one of these graphs, or all 3 at once
def SingleCurvePlot(x,y,title):
    plt.plot(x,y)
    plt.title(title)
    plt.show()
    
def DeltoidCurve():
    theta = np.arange(0,2*np.pi,.1)
    
    x = 2*(np.cos(theta)) + np.cos(2*(theta)) 
    y = 2*(np.sin(theta)) - np.sin(2*(theta)) 
    return x,y
    
def GalileanSpiral():
    theta = np.arange(0,10*np.pi,.1)
    r = theta**2
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    return x,y
    
def Fey():
    theta = np.arange(0,10*np.pi,.1)
    r = (np.e)**(np.cos(theta)) - 2*np.cos(4*theta) + (np.sin(theta/12)**5)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    return x,y
    
def All():
    x1,y1 = DeltoidCurve()
    x2,y2 = GalileanSpiral()
    x3,y3 = Fey()

    fig,axes = plt.subplots(nrows=1,ncols=3, figsize=(15,5))
    axes[0].plot(x1,y1) ; axes[0].set_title("Deltoid Curve") ; axes[0].set_aspect('equal')
    axes[1].plot(x2,y2) ; axes[1].set_title("Galilean Spiral") ; axes[1].set_aspect('equal')
    axes[2].plot(x3,y3) ; axes[2].set_title("Fey's Function") ; axes[2].set_aspect('equal')
    print("Plotting all curves...")
    plt.show()

 #argpase section
 
parser = argparse.ArgumentParser(description="Plot one of 3 curves, or all 3 at once")
parser.add_argument("curve", choices=["deltoid", "spiral", "fey", "all"], help="Choose a curve to plot: deltoid, spiral, fey, or all", type=str)
args = parser.parse_args()
print("Argument received:", args.curve) #just testing bugs, had trouble with argparse before
if args.curve == "deltoid":
    x,y = DeltoidCurve()
    SingleCurvePlot(x,y,"Deltoid Curve")
elif args.curve == "spiral":
    x,y = GalileanSpiral()
    SingleCurvePlot(x,y,"Galilean Spiral")
elif args.curve == "fey":
    x,y = Fey()
    SingleCurvePlot(x,y,"Fey's Function")
elif args.curve == "all":
    All()