from SimPy.Simulation import *

rtt_table = []

def add_rtt(rtt, srcip, dstip):
  #if(srcnode.paware and dstnode.paware):
  #  rtt_table.append((rtt, now(), 2))
  #elif(srcnode.paware or dstnode.paware):
  #  rtt_table.append((rtt, now(), 1))
  #else:
  #  rtt_table.append((rtt, now(), 0))
  rtt_table.append((rtt, now()))

def print_rtts():
  print rtt_table
