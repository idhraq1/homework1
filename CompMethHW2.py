import sys
x = float(sys.argv[1])
v = float(sys.argv[2])
te = x/v
ts = (te)*(1-(v**2))**(1/2) #in ship frame, its te times sqrt(1 - v^2 / c^2). we dont need c here since everything is in terms of c
print('It would take',ts,'years on the ship, and to someone on Earth, it would take',te,'years')