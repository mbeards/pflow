import random
import networkx as nx
from Node import *
from Link import *
from netaddr import *

#Linktable is "srcipdstip":link
linktable = {}

cbgpcommands = []

      


def setup_node(i):
  n = Node(name=("Node"+str(i)))
  n.setprefix(IPNetwork("10.0."+str(i)+"/24"))

  #cbgpcommands.append("net add node " + str(n.prefix[1]))
  cbgpcommands.append("net add node " + str(n.prefix[1]))
  #cbgpcommands.append("net add domain " + str(i))
  #cbgpcommands.append("net node " + str(n.prefix[1]) + " domain "+str(i))
  cbgpcommands.append("bgp add router " +str(i) + " "+ str(n.prefix[1]))
  cbgpcommands.append("bgp router " + str(n.prefix[1]) + " add network " + str(n.prefix))
  return n

def generate_topology(size):

  #make nodes
  nodes = [setup_node(i) for i in range(size)]

  
  g = nx.barabasi_albert_graph(size, 1)
  
  for i in range(size):
    edges = random.sample(g.nodes(), 2)
    g.add_edge(edges[0], edges[1])


  #set up links

  #foreach node
  for node in g:

    #foreach neighbor
    for neighbor in g[node].keys():
      #add a link to the neighbor
      link = Link(name=("Link"+str(node)+"-"+str(neighbor)), capacity=4) #need to vary link capacity, but don't worry yet

      #map node IPs to link pointers
      labelstr = str(nodes[node].prefix[1]) + str(nodes[neighbor].prefix[1])
      revlabelstr = str(nodes[neighbor].prefix[1]) + str(nodes[node].prefix[1])

      link.setup(nodes[neighbor], 25) #set propdelay and destination

      if(not revlabelstr in linktable):
        #Only set up the link if it doesn't already exist in reverse
        nodes[node].add_link(link) #hook link on to parent
        #add link in cbgp
        cbgpcommands.append("net add link " + str(nodes[node].prefix[1]) +" "+str(nodes[neighbor].prefix[1]))
        
      linktable[labelstr] = link
      #add static route in cbgp
      cbgpcommands.append("net node " +str(nodes[node].prefix[1]) + " route add --oif="+str(nodes[neighbor].prefix[1]) + " "+str(nodes[neighbor].prefix[1])+"/32 1")
      #set up peering
      cbgpcommands.append("bgp router " + str(nodes[node].prefix[1]) + "\n add peer " + str(neighbor) + " " + str(nodes[neighbor].prefix[1])+ "\n peer " + str(nodes[neighbor].prefix[1])+" up \n exit")

  cbgpcommands.append("sim run")

  for source in nodes:
    for destination in nodes:
      if source==destination:
        continue
      cbgpcommands.append("bgp router "+str(source.prefix[1])+" debug dp " + str(destination.prefix))
      
  return g




g = generate_topology(254)


for line in cbgpcommands:
  print line

print "sim run"

