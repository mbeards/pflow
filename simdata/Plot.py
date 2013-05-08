#!/usr/bin/python

import re
import sys
import argparse

firstlinere = re.compile("time.*")
topolinere = re.compile("Topology ([0-9]+)")
datalinere = re.compile("[0-9].*")

def main():
  runs = {}

  num = 0

  for line in sys.stdin.readlines():
    if firstlinere.match(line):
      continue
    if topolinere.match(line):
      num = num+1
    if datalinere.match(line):
      if(num in runs):
        runs[num].append(line.split())
      else:
        runs[num] = [line.split()]

  normalize(runs)
  graphruns(runs)
  overhead(runs)

def mean(l):
  return (1.0 * reduce(lambda x, y: x+y, l, 0))/len(l)

def overhead(runs):
  results = []
  print "set terminal png"
  print "set output 'overhead.png'"
  print "f(x) = m*x+c"
  print "fit f(x) '-' using 1:2 via m,c"

  for run in runs:
    #build a list of pnode counts
    rows = sorted(set(map(lambda x: x[2], runs[run])))
    probes = {} 
    maxnodes = int(runs[run][0][1])
    for row in rows:
      members=map(lambda x: float(x[8])/float(x[6]), filter(lambda x: x[2]==row, runs[run]))
      r = int(row)
      probes[r] = mean(members)
    for row in rows:
      r = int(row)
      results.append((1.0*r/maxnodes, probes[r]))
  
  for r in results:
    print r[0], r[1]
  print "end"

  print "plot '-' using 1:2, f(x)"

  for r in results:
    print r[0], r[1]
  print "end"


def normalize(runs):
  results = []
  print "set terminal png"
  print "set output 'normalized.png'"
  print "f(x) = m*x+c"
  print "fit f(x) '-' using 1:2 via m,c"

  for run in runs:
    #build a list of pnode counts
    rows = sorted(set(map(lambda x: x[2], runs[run])))
    average_rtts = {} 
    maxnodes = int(runs[run][0][1])
    for row in rows:
      members=map(lambda x: float(x[4]), filter(lambda x: x[2]==row, runs[run]))
      r = int(row)
      average_rtts[r] = mean(members)
    for row in rows:
      r = int(row)
      results.append((1.0*r/maxnodes, average_rtts[r]/average_rtts[0]))
  
  for r in results:
    print r[0], r[1]
  print "end"


  print "plot '-' using 1:2, f(x) with errorbars"

  for r in results:
    print r[0], r[1]
  print "end"

def graphruns(runs):
  for run in runs:
    print "set terminal png"
    print "set output '"+str(run)+".png'"
    print "plot '-' using 1:2"
    
    for row in runs[run]:
      print row[2], row[4]
    print "end"

  print "set output 'allruns.png'"
  print "set title 'All Runs'"
  print "plot '-' using 1:2"
  for run in runs:
    for row in runs[run]:
      print row[2], row[4]
  print "end"




main()
