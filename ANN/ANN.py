import math
import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class AN(object):
#artifical neuron

	def __init__(self):
		self.v = 0

	def update(self,v):
		self.v = self.sigmoid(v)
		#self.v = np.tanh(v)
		#self.v = v
	def sigmoid(self,x):
		return 1./(1+math.exp(-x))

class ANN(object):

	def __init__(self,n):
		self.n = n
		self.connections = {}
		self.G = nx.DiGraph()			
		for i in xrange(n):
			neuron = AN()
			self.G.add_node(neuron)
			self.connections[neuron] = [] 		

	def random_wire(self,p):
		#p is how many random connections

		for _ in xrange(p*self.n):
			neurons = self.connections.keys()
			pre = neurons[random.randint(0,self.n-1)]
			post = neurons[random.randint(0,self.n-1)]
			w = random.random()
			self.connect(pre,post,w)
			self.G.add_edge(pre,post,weight=w)			
				
	def connect(self,a,b,w):
		#connects a --> b
		self.connections[b].append((a,w)) 

	def update(self):
		old = self.connections

		for neuron in self.connections.keys():
			#print old
			input = 0
			for pre in old[neuron]:
				if pre != []:
					#print pre[0].v
					input += pre[0].v*pre[1]
					
			neuron.update(input)

	def run(self,steps):
		for _ in xrange(steps):
			self.update()

		self.prs =nx.pagerank(self.G)			
		self.close = nx.closeness_centrality(self.G)
		self.bet = nx.betweenness_centrality(self.G)
		self.katz = nx.katz_centrality(self.G)

						

nn = ANN(100)

nn.random_wire(6)

nn.run(10000)

plot = []
prs = []
close = []
bet = []
katz = []
for neuron in nn.connections.keys():
	plot.append(neuron.v)
	prs.append(nn.prs[neuron])
	close.append(nn.close[neuron])
	bet.append(nn.bet[neuron])
	katz.append(nn.katz[neuron])


plt.scatter(prs,plot)
plt.xlabel('PageRank')
plt.ylabel('Activation')
plt.show()

	
plt.scatter(close,plot)
plt.xlabel('Close')
plt.ylabel('Activation')
plt.show()

plt.scatter(bet,plot)
plt.xlabel('Bet')
plt.ylabel('Activation')
plt.show()

plt.scatter(katz,plot)
plt.xlabel('Katz')
plt.ylabel('Activation')
plt.show()

