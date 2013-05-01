from SimPy.Simulation import *

retransmission_timeout = 10



class Link(Resource):
  def setup(self, destination, delay):
    self.destination = destination
    self.delay = delay

  def __str__(self):
    return "link to " + str(self.destination)
