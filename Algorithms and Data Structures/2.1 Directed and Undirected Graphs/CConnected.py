# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np


### This is only valid for Undirected graphs since otherwise we cannot climb to the source
# of a given node.

# Well KSSCC uses it because it precomputes the parents so its ok
class CConnected(): # Finds the Clusters in G
    def __init__(self, Graph):
        self.Graph = Graph
        
    def connected(self,v, w): # is there a path from s to v?
        return self.id[v] == self.id[w]

    def DeepFirstSearch(self):  # Using DFS, when finished we check the Falses and continue
        self.marked = [False] * self.Graph.getV()
        self.id = [-1] * self.Graph.getV()   # Cluster id of the nodes
        
        self.count = 0
        # For every node, if it has not been marked yet we apply dfs to obtian all its neighbours
        for v in range(self.Graph.getV()):
            if (self.marked[v] != True):  # If we havent visited yet, we do
                self.dfs(v)
                self.count += 1;
                
    # Deep First Search recursive function
    def dfs(self,v): # Given a node
        self.marked[v] = True # It marks it as true (visited)
        self.id[v] = self.count # Specify we get to node w from v
        # Then it visits if adjacent if they havent been visited yet
        for w in self.Graph.adj(v):  
            if (self.marked[w] != True): 
                self.dfs(w)  # Visit unvisited node
                
