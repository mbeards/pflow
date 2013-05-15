#!/usr/bin/python

import re
import sys
import argparse
import math

firstlinere = re.compile("time.*")
topolinere = re.compile("Topology ([0-9]+)")
datalinere = re.compile("[0-9].*")

termstring = "set terminal postscript eps 26\nunset key"
outextension = ".eps'"

def main():
  parser = argparse.ArgumentParser(description="Plot pflow simulation data")
  parser.add_argument('--average', '-a', action='store_true')
  parser.add_argument('--norm', '-n', action='store_true')
  parser.add_argument('--overhead', '-o', action='store_true')
  parser.add_argument('--runs', '-r', action='store_true')
  parser.add_argument('--stats', '-s', action='store_true')
  parser.add_argument('--congestion', '-c', action='store_true')

  argv=parser.parse_args(sys.argv[1:]) 
  if not argv.average and not argv.norm and not argv.overhead and not argv.runs and not argv.stats and not argv.congestion:
    print "--average, --overhead, --norm"
    return

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

  if argv.norm:
    normalize(runs)

  if argv.average:
    average(runs)

  if argv.overhead:
    overhead(runs)

  if argv.runs:
    eachrun(runs)

  if argv.stats:
    stats(runs)
  
  if argv.congestion:
    congestion(runs)

def mean(l):
  return (1.0 * reduce(lambda x, y: x+y, l, 0))/len(l)

def stddev(l):
  m = mean(l)
  return math.sqrt(1.0*reduce(lambda x: x+y, map(lambda x: (x-m)**2, l))/len(l))

def overhead(runs):
  results = []
  termstring = "set terminal postscript eps 13\nunset key"
  print termstring 
  print "set output 'overhead"+outextension
  print "set xlabel 'Ratio of pflow nodes to non-pflow nodes'"
  print "set ylabel 'Probe packets sent per flow'"
  print "f(x) = m*x+c"
  print "fit f(x) '-' using 1:2 via m,c"

  for run in runs:
    #build a list of pnode counts
    rows = sorted(set(map(lambda x: x[2], runs[run])))
    probes = {} 
    maxnodes = int(runs[run][0][1])
    for row in rows:
      members=map(lambda x: float(x[8])/(2*float(x[6])), filter(lambda x: x[2]==row, runs[run]))
      r = int(row)
      probes[r] = mean(members)
    for row in rows:
      r = int(row)
      if r==0:
        results.append((0,0))
      else:
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
  termstring = "set terminal postscript eps 13\nunset key"
  print termstring
  print "set output 'normalized"+outextension
  print "set xlabel 'Ratio of pflow nodes to non-pflow nodes'"
  print "set ylabel 'Normalized RTT'"
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


  print "plot '-' using 1:2, f(x)"

  for r in results:
    print r[0], r[1]
  print "end"

def average(runs):
  results = []
  print termstring
  print "set output 'average"+outextension
  print "set xlabel 'Normalized RTT'"
  print "set ylabel 'Number of pflow nodes'"
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
      results.append((r, average_rtts[r]/average_rtts[0]))
  
  for r in results:
    print r[0], r[1]
  print "end"


  print "plot '-' using 1:2, f(x)"

  for r in results:
    print r[0], r[1]
  print "end"

def eachrun(runs):
  print termstring
  print "f(x) = m*x+c"

  for run in runs:
    results = []
    print "set output '"+str(run)+"average"+outextension
    print "set title '" + str(run) +"'"
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
      results.append((r, average_rtts[r]/average_rtts[0]))
    
    print "fit f(x) '-' using 1:2 via m,c"
      
    for r in results:
      print r[0], r[1]
    print "end"


    print "plot '-' using 1:2, f(x)"

    for r in results:
      print r[0], r[1]
    print "end"


def stats(runs):
  results = []

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
 
  #results is (pnode ratio, norm_rtt)

  q0 = map(lambda x: x[1], filter(lambda x: x[0] < .25, results))
  q1 = map(lambda x: x[1], filter(lambda x: x[0] < .5 and x[0] >=.25, results))
  q2 = map(lambda x: x[1], filter(lambda x: x[0] < .75 and x[0] >=.5, results))
  q3 = map(lambda x: x[1], filter(lambda x: x[0] < 1 and x[0] >=.75, results))
  q4 = map(lambda x: x[1], filter(lambda x: x[0] >.75, results))

  print "Normalized RTT:", 1, mean(q1), mean(q2), mean(q3), mean(q4)
  print "RTT Improvement:", 0, 1-mean(q1), 1-mean(q2), 1-mean(q3), 1-mean(q4)

  results = []

  for run in runs:
    #build a list of pnode counts
    rows = sorted(set(map(lambda x: x[2], runs[run])))
    probes = {} 
    maxnodes = int(runs[run][0][1])
    for row in rows:
      members=map(lambda x: float(x[8])/(2*float(x[6])), filter(lambda x: x[2]==row, runs[run]))
      r = int(row)
      probes[r] = mean(members)
    for row in rows:
      r = int(row)
      if r==0:
        results.append((0,0))
      else:
        results.append((1.0*r/maxnodes, probes[r]))
  
  q0 = map(lambda x: x[1], filter(lambda x: x[0] < .25, results))
  q1 = map(lambda x: x[1], filter(lambda x: x[0] < .5 and x[0] >=.25, results))
  q2 = map(lambda x: x[1], filter(lambda x: x[0] < .75 and x[0] >=.5, results))
  q3 = map(lambda x: x[1], filter(lambda x: x[0] < 1 and x[0] >=.75, results))
  q4 = map(lambda x: x[1], filter(lambda x: x[0] >.75, results))

  print "Normalized Overhead:", 1, mean(q1), mean(q2), mean(q3), mean(q4)
  
  results = []

  for run in runs:
    #build a list of pnode counts
    rows = sorted(set(map(lambda x: x[2], runs[run])))
    average_congestion = {} 
    maxnodes = int(runs[run][0][1])
    for row in rows:
      members=map(lambda x: float(x[3]), filter(lambda x: x[2]==row, runs[run]))
      r = int(row)
      average_congestion[r] = mean(members)
    for row in rows:
      r = int(row)
      if(average_congestion[0] < .05):
        continue
      elif(average_congestion[r]/average_congestion[0] <= 1):
        results.append((1.0*r/maxnodes, average_congestion[r]/average_congestion[0]))
  
  q0 = map(lambda x: x[1], filter(lambda x: x[0] < .25, results))
  q1 = map(lambda x: x[1], filter(lambda x: x[0] < .5 and x[0] >=.25, results))
  q2 = map(lambda x: x[1], filter(lambda x: x[0] < .75 and x[0] >=.5, results))
  q3 = map(lambda x: x[1], filter(lambda x: x[0] < 1 and x[0] >=.75, results))
  q4 = map(lambda x: x[1], filter(lambda x: x[0] >.75, results))

  print "Normalized Congestion:", 1, mean(q1), mean(q2), mean(q3), mean(q4)


def congestion(runs):
  results = []
  termstring = "set terminal postscript eps 13\nunset key"
  #termstring = "set terminal x11 persist"
  print termstring
  print "set output 'congestion"+outextension
  print "set xlabel 'Ratio of pflow nodes to non-pflow nodes'"
  print "set ylabel 'Normalized Congestion'"
  print "f(x) = m*x+c"
  print "fit f(x) '-' using 1:2 via m,c"

  for run in runs:
    #build a list of pnode counts
    rows = sorted(set(map(lambda x: x[2], runs[run])))
    average_congestion = {} 
    maxnodes = int(runs[run][0][1])
    for row in rows:
      members=map(lambda x: float(x[3]), filter(lambda x: x[2]==row, runs[run]))
      r = int(row)
      average_congestion[r] = mean(members)
    for row in rows:
      r = int(row)
      if(average_congestion[0] < .05):
        continue
      elif(average_congestion[r]/average_congestion[0] <= 1):
        results.append((1.0*r/maxnodes, average_congestion[r]/average_congestion[0]))
  
  for r in results:
    print r[0], r[1]
  print "end"


  print "plot '-' using 1:2, f(x)"

  for r in results:
    print r[0], r[1]
  print "end"


main()



