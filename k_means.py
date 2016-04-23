# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 14:09:21 2016

@author: steve
"""
import random
from math import sqrt
import sys
import numpy
import copy
import matplotlib

import numpy as np
import pylab as pl
import matplotlib.animation as animation

MAX_INT = 2**20;
# k-means

class InitMethod():
    random = 1
    empty = 2
    
def build_tuple(str):
    point = str.split(',')
    if len(point) != 2 :
        raise Exception("error in file data")
    # set every points to 0 cluster    
    return list([int(point[0]),int(point[1]),-1])

def read_from_file(filename):
    points = []
    with open(filename) as f:
       #line (x,y)
        for line in f.readlines():
            points.append(build_tuple(line))
    return points

def get_init_points_randomly(points,k):
    centroids = [];
    for index in range(k):
        point = points.pop();
        point[2]=index
        centroids.append(point)
    return centroids  

def get_init_points_empty(k):
    centroids = [];
    for index in range(k):
        centroids.append([0,0,0]);
    return centroids
    
def get_init_points(points,k,method):
    init_points = []
    temp_points = []
    # get the init points from various point.
    indexd = [ x for x in range(len(points))]
    random.shuffle(indexd);
    for x in indexd:
        temp_points.append(points[x])
    if method == InitMethod.random:
        init_points = get_init_points_randomly(points,k);
    if method == InitMethod.empty:
        init_points = get_init_points_empty(k);
    return init_points
    
def get_distance(point_centroid,point):
    x1 = point_centroid[0]
    y1 = point_centroid[1]
    x2 = point[0]
    y2 = point[1]
    return sqrt((x1-x2)**2+(y1-y2)**2)
    
def check_points(point,last_point):
    for index,x in enumerate(point):
        if x[2] == -1: 
            return True
        else:
            if x[2] != last_point[index][2]:
                return True
    return False     

def draw(points,centroid,k):
    style = ['b','g','r','c','m','y','k','w']
    
    pl.xlim(0,32767)
    pl.ylim(0,32767)
    
    
    for x in range(k):
        x_value = []
        y_value = []
        for point in points:
            if point[2] == x:
                x_value.append(point[0])
                y_value.append(point[1])
            if point[2] == -1:
                x_value.append(point[0])
                y_value.append(point[1])
        pl.plot(x_value,y_value,'o'+style[x])

    x_value = []
    y_value = []
    for cent in centroid:
        x_value.append(cent[0])
        y_value.append(cent[1])
        pl.plot(x_value,y_value,'x'+style[cent[2]])
    pl.show()    
    # matplotlib.animation.TimedAnimation(pl)

def run(filename,k):
    points = read_from_file(filename)   
    last_points = copy.deepcopy(points)
    k = int(k)
    centroid = get_init_points(points,k,InitMethod.random)  
    print draw(points,centroid,k)
    while (1):
        last_points = copy.deepcopy(points)
        # set the mark of each point
        for point_index in range(len(points)):
            distance = MAX_INT
            for x in centroid:
                temp_distance = get_distance(x,points[point_index]);
                if temp_distance < distance:
                    distance = temp_distance
                    centroid_index = x[2]
            points[point_index][2] = centroid_index

        if not check_points(points,last_points):
            break
        # get the minmum distance to each centroid.
        # update each centroid
        centroid = get_init_points_empty(k)
        count = [1 for x in range(k)]
        for x in points:
            for index_cluster in range(k):
                if x[2] == index_cluster:
                    centroid[index_cluster][0] = centroid[index_cluster][0]+x[0]
                    centroid[index_cluster][1] = centroid[index_cluster][1]+x[1]                    
                    count[index_cluster] = count[index_cluster]+1
        for index in range(k):
            centroid[index][0] = centroid[index][0]/count[index]
            centroid[index][1] = centroid[index][1]/count[index]
            centroid[index][2] = index
    print draw(points,centroid,k)    
         
if __name__ =='__main__':
    run(sys.argv[1],sys.argv[2])         