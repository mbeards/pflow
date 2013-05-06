from SimPy.Simulation import *

#Entry format: (timestamp, rtt, src_mode, dst_mode)
rtt_table = []


def add_rtt(rtt, srcnode, dstnode):
  rtt_table.append((now(), rtt, srcnode.paware, dstnode.paware))

def print_rtts():
  #print rtt_table

  print "Packet Count", packet_count
  print "Drop Count", drop_count
  print "Average RTT:", 1.0*rtt_sum/(1.0*len(rtt_table))

def rtt():
  rtt_sum = reduce(lambda x,y: x+(y[1]), rtt_table, 0)
  rtt_range = max(rtt_table, key=lambda x: x[1])[1] - min(rtt_table, key=lambda x: x[1])[1]
  return ((1.0*rtt_sum/(1.0*len(rtt_table))), rtt_range)

def single_rtt():
  table = filter(lambda x: (x[2] or x[3]) and x[2] != x[3], rtt_table)
  if(len(table)>0):
    rtt_sum = reduce(lambda x,y: x+(y[1]), table, 0)
    rtt_range = max(table, key=lambda x: x[1])[1] - min(table, key=lambda x: x[1])[1]
    return ((1.0*rtt_sum/(1.0*len(table))), rtt_range)
  return (0,0)

def double_rtt():
  table = filter(lambda x: x[2] and x[3], rtt_table)
  if(len(table)>0):
    rtt_sum = reduce(lambda x,y: x+(y[1]), table, 0)
    rtt_range = max(table, key=lambda x: x[1])[1] - min(table, key=lambda x: x[1])[1]
    return ((1.0*rtt_sum/(1.0*len(table))), rtt_range)
  return (0,0)


