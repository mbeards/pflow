import os
import sys

topsize = int(sys.argv[1])
botsize = int(sys.argv[2])
count = int(sys.argv[3])
interval = 1


def dosim(size, count):
  print "Running", count, "simulations of size", size
  for i in map(lambda x: interval*x, range(size+1)):
    stats = []
    for j in range(count):
      simline =  os.popen("python Simulation.py " + str(size) +" " + str(i)).read()
      #print simline
      stats.append(simline.split()) 
    #print average dropped: sum dropped / sum total
    #print average RTT: sum rtt / size
    # Experiment.size, Experiment.pnodes, Experiment.packet_count, Experiment.drop_count, Experiment.rtt()
    average_dropped = (1.0*reduce(lambda x, y: x+int(y[3]), stats, 0))/(1.0*reduce(lambda x, y: x+int(y[2]), stats, 0))
    average_rtt = (reduce(lambda x, y: x+float(y[4]), stats, 0)/count)

    print size, "nodes with", i, "paware", "drop rate", average_dropped, "rtt", average_rtt

for i in range(topsize, botsize+1):
  dosim(i, count)
