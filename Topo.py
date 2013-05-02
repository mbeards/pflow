import random
import networkx as nx
from Node import *
from Link import *
from netaddr import *

#Linktable is "srcipdstip":link
linktable = {}


      


def setup_node(i):
  n = Node(name=("Node"+str(i)))
  n.setprefix(IPNetwork("10.0."+str(i)+"/24"))
  return n

def generate_topology(size):

  #make nodes
  nodes = [setup_node(i) for i in range(size)]
  
  g = nx.barabasi_albert_graph(size, 1)

  #set up links

  #foreach node
  for node in g:

    print g[node]

    #foreach neighbor
    for neighbor in g[node].keys():
      #add a link to the neighbor
      link = Link(name=("Link"+str(node)+"-"+str(neighbor)), capacity=4) #need to vary link capacity, but don't worry yet

      #map node IPs to link pointers
      labelstr = str(nodes[node].prefix[1]) + str(nodes[neighbor].prefix[1])
      linktable[labelstr] = link

      link.setup(nodes[neighbor], 25) #set propdelay and destination
      nodes[node].add_link(link) #hook link on to parent

    
    #print the list of links
    print nodes[node].list_links()





generate_topology(254)

print linktable
