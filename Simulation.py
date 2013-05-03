from SimPy.Simulation import *
from Link import *
from Packet import *
from Node import *
import Experiment
from Topo import *

Experiment.size = int(sys.argv[1])
print "Building topology of", Experiment.size, "nodes"
nodes = generate_topology(Experiment.size)

initialize()

def runsim():
  Experiment.packet_count = 0
  Experiment.drop_count = 0

  print "Beginning simulation"

  for n in random.sample(nodes, Experiment.size/2):
    activate(n.generator, n.generator.generate(), at=0.0)

  simulate(until=100000)

  Experiment.print_rtts()

runsim()
