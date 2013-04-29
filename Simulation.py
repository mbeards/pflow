from SimPy.Simulation import *
from Link import *
from Packet import *


source_interval = 1

class PacketSource(Process):
  def generate(self, number, link):
    for i in range(number):
      p = Packet(name="Packet%02d" %(i))
      activate(p, p.move(link))
      yield hold, self, source_interval

initialize()
link = Link(5)


s = PacketSource('ps')
activate(s, s.generate(number=1000, link=link), at=0.0)

simulate(until=2000)
