from SimPy.Simulation import *
from Link import *
from Packet import *
from Node import *



initialize()


n1 = Node(name="Node1")
n2 = Node(name="Node2")
n3 = Node(name="Node3")
n4 = Node(name="Node4")

link12 = Link(name="link12", capacity=4)
link21 = Link(name="link21", capacity=3)
link12.setup(n2, 15)
link21.setup(n1, 26)
n1.add_link(link12)
n2.add_link(link21)

link13 = Link(name="link13", capacity=4)
link31 = Link(name="link31", capacity=3)
link13.setup(n3, 15)
link31.setup(n1, 26)
n1.add_link(link13)
n3.add_link(link31)

link34 = Link(name="link34", capacity=4)
link43 = Link(name="link43", capacity=3)
link34.setup(n4, 15)
link43.setup(n3, 26)
n3.add_link(link34)
n4.add_link(link43)


n1.setprefix(IPNetwork("10.1/16"))
n2.setprefix(IPNetwork("10.2/16"))
n3.setprefix(IPNetwork("10.3/16"))
n4.setprefix(IPNetwork("10.4/16"))

#load routing tables
n1.add_route(Route(IPNetwork("10.2/16"), link12, 0))
n1.add_route(Route(IPNetwork("10/8"), link13, 0))

n2.add_route(Route(IPNetwork("10/8"), link21, 0))

n3.add_route(Route(IPNetwork("10.4/16"), link34, 0))
n3.add_route(Route(IPNetwork("10/8"), link31, 0))

n4.add_route(Route(IPNetwork("10/8"), link43, 0))


activate(n1.generator, n1.generator.generate(number=400), at=0.0)
#activate(n2.generator, n2.generator.generate(number=100), at=0.0)

simulate(until=2000)
