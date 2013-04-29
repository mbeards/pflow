from SimPy.Simulation import *


retransmission_timeout = 10

class Packet(Process):
  def move(self, link):
    enqueue_time = now()
    yield request, self, link.resource
    trans_time = now()

    if(trans_time - enqueue_time > retransmission_timeout):
      yield release, self, link.resource
      return

    yield hold, self, link.propdelay
    yield release, self, link.resource
    #print now(), self.name, "Finished moving down", link.resource.name
    travel_time = now() - enqueue_time 

    #hand off the packet to the destination node
    activate(link.destination, link.destination.deliver(self))
