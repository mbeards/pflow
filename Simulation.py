from SimPy.Simulation import *
from Link import *
from Packet import *
from Node import *
import Experiment
from Topo import *
import sys

Experiment.size = int(sys.argv[1])
Experiment.pnodes = int(sys.argv[2])
#print "Building topology of", Experiment.size, "nodes with", sys.argv[2], "paware enabled"
nodes = generate_topology(Experiment.size, Experiment.pnodes)


def runsim():
  initialize()
  Experiment.packet_count = 0
  Experiment.drop_count = 0

  #print "Beginning simulation"


  for n in nodes:#random.sample(nodes, Experiment.size/2):
    activate(n.generator, n.generator.generate(), at=0.0)


  simulate(until=10000)

  #Experiment.print_rtts()
  print Experiment.size, Experiment.pnodes, Experiment.packet_count, Experiment.drop_count, Experiment.rtt()


  for n in filter(lambda x: x.paware, nodes):
    unvisitedroutes = filter(lambda x: x.visited==False, n.rib)
    if len(unvisitedroutes) > 0:
      print n, "has unvisited routes", unvisitedroutes, "full rib", n.rib
    
    unmeasuredroutes = filter(lambda x: x.rttval==999, n.rib)
    if len(unmeasuredroutes) >0:
      print n, "has unmeasured routes", unmeasuredroutes, "full rib", n.rib




runsim()
