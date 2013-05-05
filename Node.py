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
    self.rttval = 999
    self.timestamp = 0
    self.visited = False

  def rtt(self, rtt):
    self.timestamp = now()
    if self.rttval == 999:
      self.rttval = rtt
    else:
      #Moving average
      self.rttval = (0.5*rtt)+ (0.5 * self.rttval)
  
  #Takes IP as an Int!
  def match(self, ip):
    if(IPAddress(ip) in self.prefix):
      return True
    return False

  def __repr__(self):
    return str(self.prefix)+" "+str(self.link)+" rtt " + str(self.rttval)

  def __cmp__(self, other):
    if self.ip == other.ip and self.netmask==other.netmask and self.link==other.link:
      return 0
    if self.netmask > other.netmask:
      return 1
    return -1

  def __hash__(self):
   return hash(self.ip) ^ hash(self.netmask) ^ hash(self.link.destination)

class Flow:
  #expiry: 0=open, 1=matched, 2=probe sent
  def __init__(self, ip_src, ip_dst, timestamp, last_seen, route, expiry):
    self.ip_src = ip_src
    self.ip_dst = ip_dst
    self.timestamp = timestamp
    self.last_seen = last_seen
    self.route = route
    self.expiry = 0


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
    self.flow_table = []

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

  def get_route(self, ip, lasthop, packet):
    if(self.paware):
      return self.p_get_route(ip, lasthop, packet)
    routes = filter(lambda x: x.match(ip), self.rib)#and x.link.destination!=lasthop, self.rib)
    routes.sort(key=(lambda x: x.length))
    if(len(routes) == 0):
      print "Finding route to", IPAddress(ip), "from", self, "lasthop was", lasthop
      print self.rib
    return routes[-1].link

  def ftableclean(self):
    ft = filter(lambda x: (x.expiry == 2 and now()-x.timestamp > 600), self.flow_table)
    for f in ft:
      f.route.rtt(500) #300 as upper val for now.  probs needs to be proportional to table size?
      self.flow_table.remove(f)

      
    

  def p_get_route(self, ip, lasthop, packet):
    self.ftableclean()

    #check for flow table matches
    forward_matches = filter(lambda x: (x.ip_src == packet.ip_src and x.ip_dst == packet.ip_dst), self.flow_table)
    reverse_matches = filter(lambda x: (x.ip_dst == packet.ip_src and x.ip_src == packet.ip_dst), self.flow_table)

    routes = filter(lambda x: x.match(ip), self.rib)#and x.link.destination!=lasthop, self.rib)
    oldroutes = filter(lambda x: now()-x.timestamp > 100 or x.rttval == 999, routes)

    if(len(oldroutes)>0):
      outroute = routes[0]
      #print "checking", outroute
    else:
      routes.sort(key=(lambda x: x.rttval))
      outroute = routes[-1]

    if(len(forward_matches) > 0) and not packet.resp:
      f = forward_matches[0]
      if f.expiry == 1:
        f.expiry = 0
        f.timestamp = now()
      elif f.expiry == 2:
        f.expiry = 1
        return f.route.link
      else:
        if (now() - f.timestamp > 100):
          f.expiry = 2
          Experiment.packet_count = Experiment.packet_count+1
          Experiment.probe_count = Experiment.probe_count+1
          p = Packet(name="packet")
          p.ip_dst = packet.ip_dst
          p.ip_src = self.ip
          p.resp = False
          p.probe = True
          activate(p, p.run(self))

    elif(len(reverse_matches) > 0):
      #if(reverse_matches[0].expiry == 2):
        #print "ping came back"
      #also cool
      rtt = now() - reverse_matches[0].timestamp
      reverse_matches[0].route.rtt(rtt)
      self.flow_table.remove(reverse_matches[0])
    else:
      self.flow_table.append(Flow(packet.ip_src, packet.ip_dst, now(), now(), outroute, 0))

    outroute.visited = True
    return outroute.link
   
  def probe_return(self, packet):
    reverse_matches = filter(lambda x: (x.ip_dst == packet.ip_src and x.ip_src == packet.ip_dst), self.flow_table)
    if(len(reverse_matches)>0):
      rtt=now()-reverse_matches[0].timestamp
      reverse_matches[0].route.rtt(rtt)
      self.flow_table.remove(reverse_matches[0])

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
      p.probe = False

      activate(p, p.run(self.parent))
      yield hold, self, random.randint(1, 4)


