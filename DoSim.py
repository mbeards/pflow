import os
import sys

size = int(sys.argv[1])
count = int(sys.argv[2])


print "Running", count, "simulations of size", size
for i in range(size+1):
  for j in range(count):
    print os.popen("python Simulation.py " + str(size) +" " + str(i)).read()
