# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np


class CWDFO(): # Finds the direction of DGraph in a weighed graph
     # If applied to a graph with cycles, the cycles will be treated as a supernode.
     # Its components will appear in order.
    # Weighst are just ignored
     
    def __init__(self, WGraph):
        self.WGraph = WGraph
        
    def getOrder (self):
        return self.order
        
    def DeepFirstOrder(self):  # Using DFS, when finished we check the Falses and continue
        self.marked = [False] * self.WGraph.getV()
        self.id = [-1] * self.WGraph.getV()   # Cluster id of the nodes
        self.reverseOrder = []

        # For every node, if it has not been marked yet we apply dfs to obtian all its neighbours
        for v in range(self.WGraph.getV()):
            if (self.marked[v] != True):  # If we havent visited yet, we do
                self.dfs(v)
                
        self.reverseOrder.reverse()
        self.order = self.reverseOrder
    # Deep First Search recursive function
    def dfs(self,v): # Given a node 
        self.marked[v] = True # It marks it as true (visited)
        # Then it visits if adjacent if they havent been visited yet
        for w in self.WGraph.adj(v):  # Now the adjancencies are edges objects
            if (self.marked[w.vto()] != True): 
                self.dfs(w.vto())  # Visit unvisited node
        self.reverseOrder.append(v)
#        print v