import numpy as np
import networkx as nx
from pylab import *
import matplotlib.pyplot as plt
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




class inn(object):
	def __init__(self,n=100,rp = 12):
		self.rp = rp
		self.n = n #number of neurons
		self.connections = {}
		self.G = nx.DiGraph()
		for _ in xrange(n):
			neuron = izhi()
			self.G.add_node(neuron)
			self.connections[neuron] = []



	def connect(self,a,b,w):
		#a-->b
		self.connections[b].append((a,w))
	
	def random_wire(self,p):


		for i in xrange(p*self.n):
			neurons = self.connections.keys()
			pre = neurons[random.randint(0,self.n-1)]
			post = neurons[random.randint(0,self.n-1)]
			w = random.random()
			self.connect(pre,post,w)
			self.G.add_edge(pre,post,weight=w)
			#print self.connections

	def update(self):
		old = self.connections
		for neuron in self.connections.keys():

			#input = 0
			#if random.random() >= 0.5:
			input = random.random()*10
			for pre in old[neuron]:
				#print pre
				if pre != []:
					if pre[0].spikes[-1] == 1:
						input += self.rp*pre[1]
						#print input
						#print input
			neuron.update(input)


	def run(self,steps):
		for t in xrange(steps):
			self.update()

		self.katz = nx.katz_centrality(self.G)
		self.pr = nx.pagerank(self.G)	
		
'''
iz = izhi()
for t in range(10000):
	i = 0
	if random.random()>0.6:
		i = random.random()*10
	iz.update(i)
print sum(iz.spikes)
plot(iz.trace)
show()
'''

inn = inn(100)
inn.random_wire(6)

inn.run(10000)

spikes = []
katz = []
pr = []

for neuron in inn.connections.keys():
	spikes.append(sum(neuron.spikes))
	katz.append(inn.katz[neuron])
	pr.append(inn.pr[neuron])
	#print neuron.spikes


maxi = max(spikes)*1.0
spikes = [spike/maxi for spike in spikes]

plt.scatter(katz,spikes)
plt.xlabel('Katz')
plt.ylabel('#Spikes')
plt.show()


plt.scatter(pr,spikes)
plt.xlabel('PageRank')
plt.ylabel('#Spikes')
plt.show()
	
