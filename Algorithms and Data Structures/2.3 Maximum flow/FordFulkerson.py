# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np

from CEdge import *

class CFordFulkerson(): # Computes SP using BellManFord algorihtm.

    def __init__(self, FGraph):
        self.Graph = FGraph
        self.edgeTo = [-1]*FGraph.getV(); # Edge going from [v] to edgeTo[w] in the shortest path
        self.distTo = [-1]*FGraph.getV() # Distance from s to v
        
    def compute(self, s, t):
        self.value = 0.0;   # Value of the maxflow
        # While there is an augmenting path
        while (self.hasAugmentingPath(s, t)): 
            # Compute bottleneck capacity of the path
            bottle = float("inf")  
            
            # Using edgeTo[], from t to s we can travel from t to s pathway
            # and find the bottleneck
            v = t;
            while(v != s):  # While we havent touched the source
                bottle = min(bottle, self.edgeTo[v].residualCapacityTo(v)); # Check residual capacity of the edge
                v = self.edgeTo[v].other(v)  # Move to the other edge
            
            # Once we found the residual capacity, we add it to all the elements in the path
            v = t;
            while(v != s):  # While we havent touched the source
                self.edgeTo[v].addResidualFlowTo(v, bottle)
                v = self.edgeTo[v].other(v)
                # If edgeTo contains references to the edges in Graph, this will work
            
            self.value += bottle;
            print "Value Updated: " + str(self.value)
            
    def hasAugmentingPath(self, s, t):
        # Find a fucking AugmentingPath and store it in edgeTo
        # Is there a connected path between s and t which capacitis left allow us to travel ?
        # We use BFS checking also checking for the capacity constraint, if we can access t from s, then we are good
        self.edgeTo = [] # This will have the list of edges between s and t
        for i in range(self.Graph.getV()):
            self.edgeTo.append("rubish")
            
        self.marked = [0] * self.Graph.getV();  # List of intermediate touched edeges
                                            # so that we dont reprocess them again also ?
                                            # These are the ones that we can travel to from s
        
        queue = []  # List of edges in the Augmenting Path
        queue.append(s)
        self.marked[s] = True;
        
        # We perform a breath first search (BFS) from S to T and try to find a path
        # with possible flow.
        
        while (len(queue) > 0):  # While the queue is not empty
            v = queue.pop(0);
            for e in self.Graph.adj(v):  # For each edge in the adjacency of v
               w = e.other(v);             # The other edge we go to                  # found path from s to w in the residual network?
               if ((e.residualCapacityTo(w) > 0) and (self.marked[w] == False)):  # If the capacity in that direction let us continue and the edge hasent been searched already
                    self.edgeTo[w] = e;  # save last edge on path to w;
                    self.marked[w] = True;  # mark w;
                    queue.append(w); # add w to the queue
                    
        return self.marked[t];  # Return if we were able to touch t from s anyhow subject to the capacity constraints.


    def value(self):
        return self.value
        
    def inCut(self,v):   # is v reachable from s in residual network?
        # At the end of the computation, self.marked will contain the nodes in the mincut.
        return self.marked[v]

    def get_inCutV(self):
        queue = []
        for i in range (len(self.marked)):
            if(self.marked[i] == 1):
                queue.append(i)
        
        return queue