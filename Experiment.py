from SimPy.Simulation import *

#Entry format: (timestamp, rtt, src_mode, dst_mode)
rtt_table = []

def add_rtt(rtt, srcnode, dstnode):
  rtt_table.append((now(), rtt, srcnode.paware, dstnode.paware))

def print_rtts():
  print rtt_table
