from SimPy.Simulation import *
from Link import *
from Packet import *
from Node import *
import Experiment
from Topo import *


initialize()


Experiment.size = 20
print "Building topology of", Experiment.size, "nodes"
nodes = generate_topology(Experiment.size)
n1 = nodes[0]

print "Beginning simulation"
activate(n1.generator, n1.generator.generate(number=400), at=0.0)
#activate(n2.generator, n2.generator.generate(number=100), at=0.0)

simulate(until=20)

Experiment.print_rtts()
