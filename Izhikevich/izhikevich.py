import numpy as np
import networkx as nx
from pylab import *

import random
class izhi(object):
	

	def __init__(self,a=0.02,b=0.2,c=-65,d=6):
		self.a = a
		self.b = b
		self.c = c
		self.d = d



		self.trace = [0.]
		self.spikes = [0]

		self.v = -200
		self.u = b*self.v

		self.du = lambda a,b,v,u: a*(b*v-u)
	

	def update(self,I):

		self.v += (0.04*self.v**2 + 5*self.v + 140 - self.u + I)
		self.u +=  self.du(self.a, self.b, self.v, self.u)
						


		if self.v >= 30:
			self.trace.append(30)
			self.v = self.c
			self.u +=self.d
			self.spikes.append(1)

		else:
			self.trace.append(self.v)
			self.spikes.append(0)

iz = izhi()
for t in range(10000):
	i = 0
	if random.random()>0.6:
		i = random.random()*10
	iz.update(i)
print sum(iz.spikes)
plot(iz.trace)
show()


