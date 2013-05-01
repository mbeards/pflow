from SimPy.Simulation import *
from netaddr import *
import Experiment

retransmission_timeout=10

class Packet(Process):

  def run(self, startnode):

    current_node = startnode
    self.src_node = startnode
    self.timestamp = now()

    while(True):
      print self, "Arrived at", current_node.name

      #info to flowtimer goes here

      if(current_node.isowned(self.ip_dst)):
        print "Arrived at destination prefix"

        yield hold, self, 0.5
        #turn around

        if(self.resp):
          #packet is a response
          Experiment.add_rtt(now() - self.timestamp, self.src_node, self.dst_node)
          break
        self.resp = True
        tmp = self.ip_dst
        self.ip_dst = self.ip_src
        self.ip_src = tmp
        self.dst_node = current_node
        continue

      if(current_node.get_route(self.ip_dst) == None):
        break

      link = current_node.get_route(self.ip_dst)
      #transmit down link "link"
      enqueue_time = now()
      yield request, self, link #request space on the link
      send_time = now()
      #print "sent after", send_time - enqueue_time

      #drop packet if link is full, continue otherwise
      if(send_time - enqueue_time > retransmission_timeout):
        print "Dropped packet after waiting", send_time-enqueue_time
        yield release, self, link
        return
      yield hold, self, link.delay
      yield release, self, link
      travel_time = now() - enqueue_time
      #print "Sent packet in ", travel_time

      #transmission complete

      #Move to next node
      current_node = link.destination


  def __str__(self):
    return str(IPAddress(self.ip_src))+"->"+str(IPAddress(self.ip_dst))

