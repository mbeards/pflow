import random
import networkx as nx
from Node import *
from Link import *
from netaddr import *
import subprocess
import re
import sys

#Linktable is "srcipdstip":link
linktable = {}

cbgpcommands = []

route_header_re = re.compile("AS([0-9]+), AS[0-9]+:10\.0\.[0-9]+\.1, 10\.0\.([0-9])+\.0\/24")
route_re = re.compile("\*[> ] 10\.0\.[0-9]+\.0/24\t10\.0\.([0-9]+)\.1 *")

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
      labelstr = str(node) +"."+ str(neighbor)
      revlabelstr = str(neighbor) +"."+ str(node)

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
  
  cbgpcommands.append("sim run")

  p = subprocess.Popen(["cbgp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

  cbgp_stdout = p.communicate(input="\n".join(cbgpcommands))[0]
  cbgp_stdout = cbgp_stdout.splitlines()


  srcid = -1
  dstid = -1
  grab_flag = False
  allroutes = []
  state = 0




  for line in cbgp_stdout:
    if route_header_re.match(line):
      m = route_header_re.match(line)
      state = 1
      srcid = m.group(1)
      dstid = m.group(2)
      #set srcid, dstid from regex
    elif state==1 and line == "[ Current Best route: ]":
      state = 2
    elif state == 2 and route_re.match(line):
      r = route_re.match(line)
      nexthopid = r.group(1)
      l = linktable[str(srcid)+"."+str(nexthopid)]   
      bestroute = Route(IPNetwork("10.0."+str(dstid)+".0/24"), l, 0)
      state = 3
    elif state == 3 and line == "[ Shortest AS-PATH ]":
      state = 4
    elif state == 4 and route_re.match(line):
      r = route_re.match(line)
      nexthopid = r.group(1)
      l = linktable[str(srcid)+"."+str(nexthopid)]   
      rt = Route(IPNetwork("10.0."+str(dstid)+".0/24"), l, 0)
      allroutes.append(rt)
    elif state ==4 or (grab_flag and line == "Debug Decision Process" and state!=0):
      grab_flag = True
      state = 0
      if (not bestroute in allroutes):
        allroutes.append(bestroute)
      #print allroutes
      nodes[int(srcid)].rib.extend(allroutes)
      allroutes = []
      srcid = -1
      dstid = -1

  for node in nodes:
    if(len(node.rib) < size-1):
      print "Missing some routes, rebuild topology"
      exit(-1)
    
  return nodes



#g = generate_topology(int(sys.argv[1]))



