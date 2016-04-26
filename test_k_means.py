# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 15:50:45 2016

@author: steve
"""
import random
import sys
import k_means

def generate_test(size):
    with open('test_k_means.txt','w') as f:
        for x in range(int(size)-1):
            f.write("%r,%r\n" % (random.randint(0,32767),random.randint(0,32767)))
        f.write("%r,%r" % (random.randint(0,32767),random.randint(0,32767)))

if __name__ == '__main__':
    generate_test(sys.argv[1])  
    k_means.run('test_k_means.txt',sys.argv[2])