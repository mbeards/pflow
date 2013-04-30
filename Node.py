from SimPy.Simulation import *
from Packet import *
from netaddr import **

class Node:

  def __init__(self, name):
    self.name = name
    self.generator = Generator(name="packetsource")
    self.generator.parent = self

  def setlink(self,link):
    self.link = link

  def get_route(self):
    return self.link

  def setprefix(prefix):
    self.network = int(prefix.network)
    self.netmask = int(prefix.netmask)

  #Takes IP as an int!
  def isowned(ip):
    ip_masked = self.netmask & ip
    net_masked = self.netmask & self.network

    if(ip_masked == net_masked):
      return True
    return False



class Generator(Process):
  def generate(self, number):
    for i in range(number):
      p = Packet(name="packet")
      activate(p, p.run(self.parent))
      yield hold, self, 1


