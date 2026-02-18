import sys
def ShipTravel(x,v):
  te = x/v
  ts = (te)*(1-(v**2))**(1/2) #in ship frame, its te times sqrt(1 - v^2 / c^2). we dont need c here since everything is in terms of c
  print('It would take',ts,'years on the ship, and to someone on Earth, it would take',te,'years')
#argparse section
import argparse
parser = argparse.ArgumentParser(description='Calculate the time it would take for a ship to travel a distance x (in light years) given velocity v (in terms of c)')
parser.add_argument('x',type=float,help='The distance in terms of light years')
parser.add_argument('v',type=float,help='The velocity as a fraction of the speed of light')
args = parser.parse_args()
ShipTravel(args.x,args.v)
