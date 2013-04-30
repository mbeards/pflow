from SimPy.Simulation import *
from Link import *
from Packet import *
from Node import *



initialize()


#Topology :
#    link1 ->     link2->
# n1           n2       n3
#    
n1 = Node(name="Node1")
n2 = Node(name="Node2")
n3 = Node(name="Node3")

link1 = Link(name="link1", capacity=4)
link2 = Link(name="link2", capacity=3)
link1.setup(n2, 15)
link2.setup(n3, 26)
n1.setlink(link1)
n2.setlink(link2)

activate(n1.generator, n1.generator.generate(number=100), at=0.0)
#activate(n2.generator, n2.generator.generate(number=100), at=0.0)

simulate(until=2000)
