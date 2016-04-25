# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 20:55:42 2016

@author: ipprlab
"""

# test community

import random
import sys
import community

def generate_test(nodes,edges):
    node_size = int(nodes)
    edge_size = int(edges)

    with open('test_community.txt','w') as f:
        f.write("%r:%r\n" % (node_size,edge_size))       
        for x in range(1,edge_size-1):
            f.write("%r,%r\n" % (random.randint(1,node_size),random.randint(1,node_size)))
        f.write("%r,%r" % (random.randint(1,node_size),random.randint(1,node_size)))

if __name__ == '__main__':
    generate_test(sys.argv[1],sys.argv[2])       
    community.main('test_community.txt',3)    