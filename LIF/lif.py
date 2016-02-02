from numpy import *
from pylab import *
import matplotlib.pyplot as plt
import networkx as nx
import random

class lif(object):


	def __init__(self,ref=10,Cm=10.,Rm=1.,th=1.2,spike=0.8,dt=0.125):
		self.ref = ref #refactory period (msec)
		self.Cm = Cm #capacitance (uF)
		self.Rm = Rm #resitance (kOhm)
		self.th = th #threshold (V)
		self.spike = spike #how much the neuron spikes
		self.tau = Rm*Cm #time constant (msec)
		self.t_rest = 0. #inital refactory
		self.trace = [0.] #put membrane potential in there
		self.dt = dt
		self.spikes = [0] #spike train
		self.t= 1
	def update(self,I): 
		#I= input current
		#t = current time step
		if self.t >= self.t_rest:
			vt = self.trace[self.t-1] + (-self.trace[self.t-1] + I*self.Rm) / self.tau #* self.dt  
			if vt >= self.th:
				vt += self.spike
				self.spikes.append(1)
				self.t_rest = self.t + self.ref
				#print self.t_rest - self.t
			else:
				self.spikes.append(0)

			self.trace.append(vt)
		else:
			self.trace.append(0)
			self.spikes.append(0)

		self.t +=1
class lnn(object):


	def __init__(self,n=100,rp = 1.5):
		self.rp = rp
		self.n = n #number of neurons
		self.connections = {}
		self.G = nx.DiGraph()
		for _ in xrange(n):
			neuron = lif()
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
			input = random.random()*2.5
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
#lifn = lif()

#for t in xrange(1000):
#	lifn.update(1.5)
#plot(lifn.trace)
#show()

if name == "__main__":
	lnn = lnn(100)

	lnn.random_wire(6)

	lnn.run(200000)

	spikes = []
	katz = []
	pr = []
	for neuron in lnn.connections.keys():
		spikes.append(sum(neuron.spikes))
		katz.append(lnn.katz[neuron])
		pr.append(lnn.katz[neuron])
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
		
