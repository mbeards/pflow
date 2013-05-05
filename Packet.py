from SimPy.Simulation import *
from netaddr import *
import Experiment

retransmission_timeout=10

class Packet(Process):

  def run(self, startnode):

    current_node = startnode
    last_node = None
    self.src_node = startnode
    self.timestamp = now()

    while(True):

      #Handle arrival at destination prefix
      if(current_node.isowned(self.ip_dst)):

        yield hold, self, 0.5

        if(self.resp):
          #packet is a response
          Experiment.add_rtt(now() - self.timestamp, self.src_node, self.dst_node)
          if self.probe:
            current_node.probe_return(self)

          break
        self.resp = True
        tmp = self.ip_dst
        self.ip_dst = self.ip_src
        self.ip_src = tmp
        self.dst_node = current_node
        self.last_node = None
        continue

      #if(current_node.get_route(self.ip_dst, last_node) == None):
      #  print "Dropped packet: unavailable route"
      #  break

      link = current_node.get_route(self.ip_dst, last_node, self)
      yield hold, self, current_node.forward_delay
      #transmit down link "link"
      enqueue_time = now()
      yield request, self, link #request space on the link
      send_time = now()
      #print "sent after", send_time - enqueue_time

      #drop packet if link is full, continue otherwise
      if(send_time - enqueue_time > retransmission_timeout):
        #print "Dropped packet after waiting", send_time-enqueue_time
        Experiment.drop_count = Experiment.drop_count+1
        yield release, self, link
        return
      yield hold, self, link.delay
      yield release, self, link
      travel_time = now() - enqueue_time
      #print "Sent packet in ", travel_time

      #transmission complete

      #Move to next node
      last_node = current_node
      current_node = link.destination


  def __str__(self):
    s = ""
    if self.probe:
      s="p"
    return str(IPAddress(self.ip_src))+"->"+str(IPAddress(self.ip_dst))+s

