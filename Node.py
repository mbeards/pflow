from SimPy.Simulation import *
from Packet import *

class Node:

  def __init__(self, name):
    self.name = name
    self.generator = Generator(name="packetsource")
    self.generator.parent = self

  def setlink(self,link):
    self.link = link

  def get_route(self):
    return self.link

class Generator(Process):
  def generate(self, number):
    for i in range(number):
      p = Packet(name="packet")
      activate(p, p.run(self.parent))
      yield hold, self, 1


