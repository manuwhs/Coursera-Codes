# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import UF as UF
import Queue 
from CEdge import *
import CMinPQ as MPQ
# Krustal Algo to compute the MST

class CKDijkstraSP(): # Computes MST
    def __init__(self, WGraph):
        self.Graph = WGraph
        self.edgeTo = [-1]*WGraph.getV(); # Edge going from [v] to edgeTo[w] in the shortest path
        self.distTo = [-1]*WGraph.getV() # Distance from s to v
        
    def relax(self, e):
        # Relaxes a node for the edgeTo and distTo structure 
        v = e.vfrom()
        w = e.vto();
        
#        print v,w
        # If the distance to go to w using the new edge "e" is lower than the previous one
        # We set the new edge to go to w
        if (self.distTo[w] > self.distTo[v] + e.weight()):
            self.distTo[w] = self.distTo[v] + e.weight();
            self.edgeTo[w] = v;
        
            # Update paths in the priority queue
            if (self.pq.contains(w)):  
                self.pq.decreaseKey(self.distTo[w], w);
            else:
                self.pq.insert(self.distTo[w], w);

    def computeSP(self,s):
        self.s = s;  # Source node 
        self.pq = MPQ.CMinPQ();  #pq to have ordered shit
        self.visited = [0] * self.Graph.getV()
        # We will process the nodes that are closer to the source first.
        
        # Initialize disTo
        self.distTo[s] = 0.0;
        for v in range (self.Graph.getV()):
            self.distTo[v] = float('Inf')
            
        # Initialize queue of nodes to process
        self.pq.insert(0.0, s);  # Insert the node itself to the priority queue
        self.distTo[s] = 0.0
        
        while (self.pq.isEmpty() != True):  # While there are nodes to process
            # Get the closest node to S
            v = self.pq.delMin()[1];   # Gets the minimum element and removes it from the queue
                # Position [1] coz it is key,value
            self.visited[v] = 1
            print "Processing node:" + str(v)
            
            for e in self.Graph.G[v]:  # For every edge going from the node v
            # We have to keep a list of visited nodes.            
                if (self.visited[e.vto()] == 0): # If we havent visited the node we are going to
                    self.relax(e);  # Relax the edge

            
        return self.distTo, self.edgeTo