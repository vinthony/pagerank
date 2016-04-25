#!/usr/bin/env python
from __future__ import division
import numpy as np 
import sys
import os
import time
import math

def init():
	#delete_cache()
	os.mkdir('cache')

def init_r_old(non):
	r_old_init = 1/float(non)
	with open('cache/rold.txt','w') as f:
		#save each part of r-old to the file
		for x in range(non):
			f.write('%r\n' % r_old_init)


def calculate_r_new(rold,beta):
	with open('cache/rold.txt') as rold:
		r_old = [x for x in rold.readlines()];
	r_new = [(1-beta)/len(r_old) for x in range(len(r_old))]
	with open('cache/M.txt') as m:
		for m_line in m.readlines():
			source,degree,destination = m_line.split(",")
			source = int(source)
			degree = int(degree)
			destination = [int(x) for x in destination.replace("'","").split(':')]
			for item in destination:
				r_new[item] = r_new[item]+float(r_old[source])/degree 
	with open('cache/rnew.txt','w') as rnew:
		for x in r_new:
			rnew.write('%r\n'% x)
	
def get_tolerate():
	with open('cache/rold.txt') as rold:
		rold = rold.readlines()
	with open('cache/rnew.txt') as rnew:
		rnew = rnew.readlines()
	tolerate = sum([math.fabs(float(rold[index])-float(rnew[index])) for index in range(len(rold))])
	return tolerate

def delete_cache():
	#delete file first
	os.rmdir('cache')

def readfromfile(filename):
	# need to calculator :
	# the number of nodes
	# if the number of edges is bigger than main memory , we could save it to a file
	# according the index of each node.
	non = 0 #number of nodes
	noe = 0 #number of edges
	edges = [] # edges(x,y) directed graph
	each_block = 0
	lines = [];
	cache_line = {}
	with open(filename) as f:
		lines = f.readlines();
		# according the file size to determine main memory or file.
		for line in lines:
			#print cache_line
			M = "";
			if ":" in line:
				non,noe = [int(x) for x in line.split(':')]
			else:
				# edges
				x,y = [int(x) for x in line.split('\t')] # x is source
				destination = [y]
				if cache_line.has_key(str(x)):
					continue
				for item in lines:
					if ':' in item:
						continue;
					x1,y1 = [int(w) for w in item.split('\t')]
					if x1 == x and y1 != y:
						destination.append(y1)
				M = "%r,%r,%r\n" % (x,len(destination),':'.join([str(m) for m in destination]))
				cache_line[str(x)] = 1;
				with open('cache/M.txt','a') as m:
					m.write(M)		
		return non
def set_to_new(x):
	# delete r_old 
	# r_new = r_old
	os.rename('cache/rold.txt','cache/rold-%r.txt'% x)
	os.rename('cache/rnew.txt','cache/rold.txt')

def vis():
	pass

def run(filename,beta):
	elps = 0.0001
	before = time.time()
	tolerate = 2**20
	# calculator the d of each 
	# assuming the calculator is more than main memory, so we could store the D map to disk
	init()
	number_of_nodes=readfromfile(filename)
	r_old = init_r_old(number_of_nodes)
	count = 0;
	while 1:
		# recalculate
		calculate_r_new(r_old,beta)	
		tolerate = get_tolerate()
		if tolerate < elps:
			break
		set_to_new(count)
		count =  count + 1
	end = time.time()
	vis()
	#delete_cache()
	print 'cost:%r' % (end-before)
if __name__ == '__main__':
	run(sys.argv[1],sys.argv[2])
	#readfromfile()