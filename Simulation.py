from SimPy.Simulation import *
from Link import *
from Packet import *
from Node import *
import Experiment
from Topo import *
import sys
import copy

Experiment.size = int(sys.argv[1])
Experiment.weightavg = 0
#Experiment.pnodes = int(sys.argv[2])
#print "Building topology of", Experiment.size, "nodes with", sys.argv[2], "paware enabled"
nodes = generate_topology(Experiment.size)


def runsim(g):
  initialize()
  Experiment.packet_count = 0
  Experiment.drop_count = 0

  #print "Beginning simulation"
  nodes = setup_nodes(g, Experiment.size, Experiment.pnodes)


  for n in nodes:#random.sample(nodes, Experiment.size/2):
    activate(n.generator, n.generator.generate(), at=0.0)


  simulate(until=10000)

  #Experiment.print_rtts()
  print Experiment.size, Experiment.pnodes, Experiment.weightavg, Experiment.packet_count, Experiment.drop_count, Experiment.rtt()


  for n in filter(lambda x: x.paware, nodes):
    unvisitedroutes = filter(lambda x: x.visited==False, n.rib)
    if len(unvisitedroutes) > 0:
  #    print n, "has unvisited routes", unvisitedroutes, "full rib", n.rib
      return -1
    
    unmeasuredroutes = filter(lambda x: x.rttval==999, n.rib)
    if len(unmeasuredroutes) >0:
  #    print n, "has unmeasured routes", unmeasuredroutes, "full rib", n.rib
      return -1

  #for n in nodes:
  #  print n.rib



for i in range(Experiment.size+1):
  Experiment.pnodes = i
  val = runsim(nodes)
