from SimPy.Simulation import *

#Entry format: (timestamp, rtt, src_mode, dst_mode)
rtt_table = []


def add_rtt(rtt, srcnode, dstnode):
  rtt_table.append((now(), rtt, srcnode.paware, dstnode.paware))

def print_rtts():
  #print rtt_table

  rtt_sum = reduce(lambda x,y: x+(y[1]), rtt_table, 0)

  print "Packet Count", packet_count
  print "Drop Count", drop_count
  print "Average RTT:", 1.0*rtt_sum/(1.0*len(rtt_table))

