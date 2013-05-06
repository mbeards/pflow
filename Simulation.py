from SimPy.Simulation import *
from Link import *
from Packet import *
from Node import *
import Experiment
from Topo import *
import sys
import copy
from datetime import datetime

if(len(sys.argv) < 4):
  print "Usage: python " + sys.argv[0] + "TopologySize TopologyCount Iterations"
  exit()

Experiment.size = int(sys.argv[1])
topologies = int(sys.argv[2])
iterations = int(sys.argv[3])

Experiment.weightavg = 0
Experiment.m = False
#Experiment.pnodes = int(sys.argv[2])
#print "Building topology of", Experiment.size, "nodes with", sys.argv[2], "paware enabled"

def stats():
  congestion = (1.0*Experiment.drop_count)/Experiment.packet_count
  overall_rtt = Experiment.rtt()
  single_rtt = Experiment.single_rtt()
  double_rtt = Experiment.double_rtt()

  return " ".join(map(str,[congestion, overall_rtt[0], overall_rtt[1], single_rtt[0], single_rtt[1], double_rtt[0], double_rtt[1]]))

def runsim(g):
  starttime = datetime.now()
  initialize()
  Experiment.packet_count = 0
  Experiment.drop_count = 0
  Experiment.probe_count = 0
  Experiment.current = 0
  Experiment.old = 0

  #print "Beginning simulation"
  nodes = setup_nodes(g, Experiment.size, Experiment.pnodes)


  for n in random.sample(nodes, Experiment.size/2):
    activate(n.generator, n.generator.generate(), at=0.0)


  simulate(until=10000)

  print (datetime.now()-starttime), Experiment.size, Experiment.pnodes, stats()


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


for j in range(topologies):
  print "Topology", j
  nodes = generate_topology(Experiment.size)
  for i in range(Experiment.size+1):
    if(Experiment.size > 10 and i%5 != 0):
      continue
    if(Experiment.size <= 10 and i%2 != 0):
      continue
    Experiment.pnodes = i
    for k in range(iterations):
      val = runsim(nodes)
    #  if i>0:
    #    Experiment.m = True
    #    val = runsim(nodes)
    #    Experiment.m = False

