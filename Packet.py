from SimPy.Simulation import *

retransmission_timeout=10

class Packet(Process):

  def run(self, startnode):

    current_node = startnode

    while(True):
      link = current_node.get_route()
      #transmit down link "link"
      enqueue_time = now()
      yield request, self, link #request space on the link
      send_time = now()
      print "sent after", send_time - enqueue_time

      #drop packet if link is full, continue otherwise
      if(send_time - enqueue_time > retransmission_timeout):
        print "Dropped packet after waiting", send_time-enqueue_time
        yield release, self, link
        return
      yield hold, self, link.delay
      yield release, self, link
      travel_time = now() - enqueue_time
      print "Sent packet in ", travel_time

      #transmission complete

      #At the next node
      current_node = link.destination
      print "Arrived at", current_node.name

      if(current_node.get_route() == None):
        break




