from SimPy.Simulation import *

class Link:
  def __init__(self, propdelay, destination):
    self.destination = destination
    self.propdelay = propdelay
    self.resource = Resource(capacity=3)
