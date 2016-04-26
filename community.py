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
				updated_weight = weight + node_edge
				#if min_value > updated_weight:
				min_value = updated_weight
				node_next = node_to		
			if node_next != 0 and min_value != INT_MAX:
				q.put((updated_weight,node_next))
				if path.has_key((from_node,node)):
					path[(from_node,node_next)] = path[(from_node,node)] +":"+'%r,%r'% (node,node_next)
				else:
					path[(from_node,node_next)] = '%r,%r'% (node,node_next)
	return path

def remove_x_from_edges(cutted,edges):
	node_from,node_end = [int(x) for x in cutted.split(',')]
	for edge in edges:
		if edge[0] == node_from and edge[1] == node_end:
			edges.remove(edge)
	return edges		

def readfromfile(filename):
	edges = []
	with open(filename) as f:
		for line in f.readlines():
			if ":" in line:
				nodes_number,edge_number = [int(x) for x in line.split(':')]
			else:
				splited_line = line.split(',');
				from_node,to_node = [item for item in splited_line]
				edges.append((int(from_node),int(to_node),float(1))) # weight always equals 1
	nodes = [x for x in range(1,nodes_number)]
	return nodes,edges		

# def get_cluster(edges,):
		# return the new cluster of edges

def main(filename):
	nodes,edges = readfromfile(filename)
	nodes_associate = []
	betweeness = {}
	cutted = "";
	final = [];
	# G = nx.DiGraph()
	# G.add_nodes_from(nodes)
	# G.add_weighted_edges_from(edges)
	# position = nx.nx_agraph.graphviz_layout(G)
	# nx.draw_networkx_edges(G,pos=position,edgelist=edges,arrows=False)
	while(1):
		betweeness.clear()
		nodes_associate = []
		temp_value = - INT_MAX
		final_value = - INT_MAX
		for node in nodes:
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
		print "cutted:%r,betweeness:%r" % (cutted,betweeness[cutted])		
		edges = remove_x_from_edges(cutted,edges);
		final.append(cutted)	
		if not edges:
			break
			 
if __name__ == '__main__':
	main(sys.argv[1])