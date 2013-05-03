from SimPy.Simulation import *
from Packet import *
from netaddr import *
import random

class Route:
  def __init__(self, prefix, link, hopcount):
    self.ip = int(prefix.ip)
    self.netmask = int(prefix.netmask)
    self.prefix = prefix
    self.length = prefix.prefixlen
    self.link = link
    self.hopcount = hopcount
    self.rttval = -1
  
  #Takes IP as an Int!
  def match(self, ip):
    if(IPAddress(ip) in self.prefix):
      return True
    return False

  def __repr__(self):
    return str(self.prefix)+" "+self.link.name+" "+str(self.hopcount)

  def __cmp__(self, other):
    if self.ip == other.ip and self.netmask==other.netmask and self.link==other.link:
      return 0
    if self.netmask > other.netmask:
      return 1
    return -1

  def __hash__(self):
    return hash(self.ip) ^ hash(self.netmask) ^ hash(self.link.destination)


class Node:
  def __init__(self, name):
    self.name = name
    self.generator = Generator(name="packetsource")
    self.generator.parent = self
    self.links = []
    self.ip = 0
    self.netmask = 0
    self.prefix = None
    self.rib = []
    self.paware = False
    self.forward_delay = random.randint(0,5)

  def __repr__(self):
    if(self.paware):
      return "Paware " + self.name +" "+str(self.prefix) + "\n"+str(self.rib)
    else:
      return "naware " + self.name +" "+str(self.prefix)+"\n" + str(self.rib)

  def list_links(self):
    return str(self.links)

  def add_link(self, l):
    self.links.append(l)

  def add_route(self, r):
    self.rib.append(r)

  def get_route(self, ip, lasthop, packet):
    #print "\nEntire RIB", self.rib
    routes = filter(lambda x: x.match(ip), self.rib)#and x.link.destination!=lasthop, self.rib)
    #print "All routes to", IPAddress(ip), ":", routes
    routes.sort(key=(lambda x: x.length))
    #print "Best route to", IPAddress(ip), "is", routes[-1]
    if(len(routes) == 0):
      print "Finding route to", IPAddress(ip), "from", self, "lasthop was", lasthop
      print self.rib
    return routes[-1].link
    

    return self.link

  def setprefix(self, prefix):
    self.ip = int(prefix.ip)
    self.netmask = int(prefix.netmask)
    self.prefix = prefix

  #Takes IP as an int!
  def isowned(self, ip):
    if (IPAddress(ip) in self.prefix):
      #print IPAddress(ip), "is in",self.prefix
      return True
    #print IPAddress(ip), "is not in", self.prefix
    return False


class Generator(Process):
  def generate(self):
    while(True):
      Experiment.packet_count = Experiment.packet_count+1
      addr = random.randint(0,Experiment.size-1)
      ipstr = "10.0."+str(addr)+".1"

      p = Packet(name="packet")
      p.ip_dst = int(IPAddress(ipstr))
      p.ip_src = self.parent.ip
      p.resp = False

      activate(p, p.run(self.parent))
      yield hold, self, random.randint(1, 4)


