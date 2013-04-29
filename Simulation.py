from SimPy.Simulation import *
from Link import *
from Packet import *
from Node import *



initialize()


#Topology :
#    link1 -> 
# n1           n2
#    <- link2
n1 = Node(name="LeftNode")
n2 = Node(name="RightNode")
link1 = Link(name="link1", capacity=4)
link2 = Link(name="link2", capacity=3)
link1.setup(n2, 15)
link2.setup(n1, 26)
n1.setlink(link1)
n2.setlink(link2)

activate(n1.generator, n1.generator.generate(number=100), at=0.0)
activate(n2.generator, n2.generator.generate(number=100), at=0.0)

simulate(until=2000)
