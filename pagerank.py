#!/usr/bin/env python

from __future__ import division
import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def v_v(v1,v2):
    s = 0
    for x in range(0, len(v1)):
        s += v1[x]*v2[x]
    return s

def m_v(M1,v,beta,topic):
    re = []
    length = len(v)
    for x in range(0,length):
        m = M1[x*length:(x+1)*length]
        if x in topic:
            re.append(v_v(m,v)*beta+(1-beta)/len(topic))    
        else:
            re.append(v_v(m,v)*beta)    
    return re

def getcontentfromfile(filename):
    with open(filename) as f:
        contents = f.readlines()
    re = {}
    re['beta'] = float(contents[0])
    le = int(contents[1])
    re['length'] = le
    matrix = [0 for x in range(0, le*le)]
    f = {}
    re['graphs'] = []
    vector = [1/le for x in range(0,le)]

    for x in range(0,le+1):
        f[x] = []
    for item in contents[3:]:
        temp = [int(x) for x in item.split(' ')]
        f[temp[0]].append(temp[1])
        re['graphs'].append(tuple([temp[0],temp[1]]))

    for index,x in f.items():
        if index == 0:
            continue
        temp_length = len(x) 
        i = 1/temp_length
        for y in x:
            matrix[(index-1)+(y-1)*le] = i
    re['matrix'] = matrix
    re['vector'] = vector
    re['topic'] = [ int(x) for x in contents[2].split(' ')]
    return re
    
def getdiff(v0,v1):
    re = 0
    for index,x in enumerate(v0):
        re += abs(v0[index]-v1[index])
    return re

def calculator(tolerate,content):
    f = content['vector']
    diff = 1
    count = 0
    while(diff > tolerate):
        f_new = m_v(content['matrix'],f,content['beta'],content['topic'])
        diff = getdiff(f,f_new)
        f = f_new
        count = count+1
    G = nx.MultiDiGraph()
    for x in content['graphs']:
        G.add_edge(x[0],x[1])
    label = dict((n,f[n-1]) for n in range(1,len(f)+1))
    pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw_networkx_nodes(G,pos)
    nx.draw_networkx_labels(G,pos,label)
    nx.draw_networkx_edges(G,pos)
    plt.show()
    print "iterator:%rtimes,beta:%r,topic:%r,result:%r" % (count,content['beta'],content['topic'],f)


def run():
    tolerate = 0.00001
    filename = sys.argv[1]
    content = getcontentfromfile(filename)
    calculator(tolerate,content)


if __name__ == '__main__':
    run()
