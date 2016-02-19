#!/usr/bin/env python

from __future__ import division
import sys


def v_v(v1,v2):
    s = 0;
    for x in range(0,len(v1)):
        s += v1[x]*v2[x]
    return s;

def m_v(M1,v,beta,topic):
    re = []
    length = len(v)
    for x in range(0,length):
        m = M1[x*length:(x+1)*length]
        if x in topic:
            re.append(v_v(m,v)*beta+(1-beta)/len(topic))    
        else:
            re.append(v_v(m,v)*beta)    
    return re;

def getcontentfromfile(filename):
    with open(filename) as f:
        contents = f.readlines()
    re = {};
    re['beta'] = float(contents[0])
    le  = int(contents[1])
    re['length'] = le
    fin = [ 0 for x in range(0,le*le)] 
    f = {}
    w = []
    for x in range(0,le):
        f[x] = []
        w.append(1/le)   
    for item in contents[3:]:
        temp = [int(x) for x in item.split(' ')]
        f[temp[0]].append(temp[1])
    for index,x in f.items():
        temp_length = len(x) 
        i = 1/temp_length
        for y in x:
            fin[index+y*le] = i
    re['g'] = fin
    re['f'] = w   
    re['topic'] = [ int(x) for x in contents[2].split(' ') ]   
    return re

def calculator(times,content):
    f = content['f']
    while(times):
        f = m_v(content['g'],f,content['beta'],content['topic'])
        times = times -1
    print "topic:%r,beta:%r,result:%r" % (content['beta'],content['topic'],f)


def run():
    times = 1000;
    filename = sys.argv[1]
    content = getcontentfromfile(filename)
    calculator(times,content)



if __name__ == '__main__':
    run();
