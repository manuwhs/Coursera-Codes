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

class CBellmanFord(): # Computes SP using BellManFord algorihtm.

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
            self.changing[w] = 1  # We changed its value

    def computeSP(self,s):
        self.s = s;  # Source node 
        self.pq = MPQ.CMinPQ();  #pq to have ordered shit
        self.changed = [1] * self.Graph.getV()  # List of the edged that were changed in the last i
        # Initialized with 1 because in the first run we check all edges
        self.changing = [0] * self.Graph.getV() # List of the edges changing in this i
        # We will process the nodes that are closer to the source first.
        
        # Initialize disTo
        self.distTo[s] = 0.0;
        for v in range (self.Graph.getV()):
            self.distTo[v] = float('Inf')
            
        # Initialize queue of nodes to process
        self.distTo[s] = 0.0
        
        for i in range (self.Graph.getV()):
            for v in range (self.Graph.getV()):
                if (self.changed[v] == 1): # Only check if it was changed in last i
                    print "Processing node:" + str(v)
                    for e in self.Graph.G[v]:  # For every edge going from the node v         
                        self.relax(e);  # Relax the edge
                        
            # Negative cycle detection:
            # Check that no vertex lower than i has been updated
            
            for j in range(i):
                if (self.changing[j] == 1):
                    print "Negative Cycle at " + str(j)
                    
                    ## TraceBack of Negative Cycle
                    start_v = self.edgeTo[j] # The one previous to the v updated
                    next_v = self.edgeTo[start_v] 
                    print start_v
                    # Look into the loop until we give a vuelta
                    while(next_v != start_v):
                        print next_v
                        next_v = self.edgeTo[next_v]
                    
                    return self.distTo, self.edgeTo
                    
            self.changed = copy.deepcopy(self.changing)
            
            self.changing = [0] * self.Graph.getV()
#            print self.changed 
            
        return self.distTo, self.edgeTo