from SimPy.Simulation import *
from Packet import *
from netaddr import *

class Route:
  def __init__(self, prefix, link, hopcount):
    self.ip = int(prefix.ip)
    self.netmask = int(prefix.netmask)
    self.prefix = prefix
    self.length = prefix.prefixlen
    self.link = link
    self.hopcount = hopcount
  
  #Takes IP as an Int!
  def match(self, ip):
    if(ip & self.netmask == self.ip & self.netmask):
      return True
    return False

  def __repr__(self):
    return str(self.prefix)+" "+self.link.name


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

  def __repr__(self):
    if(self.paware):
      return "Paware " + self.name +" "+str(self.prefix)
    else:
      return "naware " + self.name +" "+str(self.prefix)

  def list_links(self):
    return str(self.links)

  def add_link(self, l):
    self.links.append(l)

  def add_route(self, r):
    self.rib.append(r)

  def get_route(self, ip):
    print "\nEntire RIB", self.rib
    routes = filter(lambda x: x.match(ip), self.rib)
    print "All routes to", IPAddress(ip), ":", routes
    routes.sort(key=(lambda x: x.length))
    print "Best route to", IPAddress(ip), "is", routes[-1]
    return routes[-1].link
    

    return self.link

  def setprefix(self, prefix):
    self.ip = int(prefix.ip)
    self.netmask = int(prefix.netmask)
    self.prefix = prefix

  #Takes IP as an int!
  def isowned(self, ip):
    if (IPAddress(ip) in self.prefix):
      print IPAddress(ip), "is in",self.prefix
      return True
    print IPAddress(ip), "is not in", self.prefix
    return False


class Generator(Process):
  def generate(self, number):
    for i in range(number):
      if(i==0):
        continue
      ipstr = "10."+str((i%4)+1)+".0.1"

      p = Packet(name="packet")
      p.ip_dst = int(IPAddress(ipstr))
      p.ip_src = self.parent.ip
      p.resp = False

      activate(p, p.run(self.parent))
      yield hold, self, 1


