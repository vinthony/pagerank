#!/usr/bin/env python

# for every node , calculator each node's shortest path to each other node.
# so there will be a shortest path list with all the nodes.
# calculator the betweeness of edges by scan each shortest path.
# detemine which edge to cut .
# repeat.
import sys
import Queue
import numpy
import matplotlib

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

INT_MAX = 2**20

def vis():
	pass
#edges
# tuple(from,to,weight)
# calculator each node from from_node to anyother node 
def bfs(from_node,edges):
	q = Queue.PriorityQueue()
	q.put((1,from_node))
	path = {}		
	while not q.empty():
		node_next = 0
		updated_weight = INT_MAX
		weight,node = q.get();
		min_value = INT_MAX
		for edge in edges: #search each edges 
			node_from,node_to,node_edge = edge
			if node == node_from: # calculate the end node. adjusted
				updated_weight = weight + node_edge['weight']
				#if min_value > updated_weight:
				min_value = updated_weight
				node_next = node_to		
			if node_next != 0 and min_value != INT_MAX:
				q.put((updated_weight,node_next))
				if path.has_key((from_node,node)):
					path[(from_node,node_next)] = path[(from_node,node)] +":"+'%r,%r'% (node,node_next)
				else:
					path[(from_node,node_next)] = '%r,%r'% (node,node_next)
	#key(x,y):[(1,2),(2,3),(3,4)]	
	return path

def remove_x_from_edges(cutted,edges):
	node_from,node_end = [int(x) for x in cutted.split(',')]
	for edge in edges:
		if edge[0] == node_from and edge[1] == node_end:
			edges.remove(edge)
	return edges		

def readfromfile(filename):
	edges = []
	nodes = []
	with open(filename) as f:
		for line in f.readlines():
			if ":" in line:
				nodes_number,edge_number = [int(x) for x in line.split(':')]
			else:
				from_node,to_node = [int(item) for item in line.split(',')]
				edges.append((from_node,to_node,{'weight':1})) # weight always equals 1
				if from_node not in nodes:
					nodes.append(from_node)
	return nodes,edges		


def main(filename,cluster):
	nodes,edges = readfromfile(filename)
	nodes_associate = []
	betweeness = {}

	cutted = "";
	final = [];
	# G = nx.Graph()
	# G.add_nodes_from(nodes)
	# G.add_edges_from(edges)
	# plt.show()
	# nodes=nx.draw_networkx_nodes(G,pos=nx.spring_layout(G)).get_paths()
	# nx.draw_networkx_labels(G,nodes)
	# nx.draw_spectral(G,hold=True)
	# plt.savefig("path.png")
	while(1):
		betweeness.clear()
		nodes_associate = []
		temp_value = - INT_MAX
		final_value = - INT_MAX
		for node in nodes:
			#calculator each node's shortest path to anyother nodes.
			paths = bfs(node,edges)
			nodes_associate.append(paths)
		for ass in nodes_associate:
			for key,value in ass.iteritems():
				for item in value.split(':'):
					if betweeness.has_key(item):
						betweeness[item] = betweeness[item] + 1
					else:
						betweeness[item] = 1
		for key,value in betweeness.iteritems():
			temp_value = value
			if  final_value < temp_value: # find the maxmum betweeness of key.
				final_value = temp_value
				cutted = key
		print betweeness
		print "cutted:%r,betweeness:%r" % (cutted,betweeness[cutted])		
		edges = remove_x_from_edges(cutted,edges);
		final.append(cutted)	
		if len(edges) - int(cluster) < 0:
			break
	for x in final:
		print x		
			 
if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2])