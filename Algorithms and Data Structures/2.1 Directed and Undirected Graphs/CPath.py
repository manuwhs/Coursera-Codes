# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np

class CPath(): # find paths in G from source s:  Finds Nodes reachable from S and the path
    def __init__(self, Graph, s):
        self.Graph = Graph
        self.s = s
        
    def hasPathTo(self,v): # is there a path from s to v?
        return self.marked[v]
        
    def pathTo(self,v):    # path from s to v; null if no such path
        if (self.hasPathTo(v) == False):
            return [];  # No way
        elif (v == self.s):
            return [s]
        # We run from v to s using the edgeTo
        path = [v]
        w = self.edgeTo[v]
        
        while (w != self.s):
           path.append(w)
           w = self.edgeTo[w]
           
        path.append(w)
         
        return path
    
    def DeepFirstSearch(self):  # Does not guarantee minimum length in the path
        self.marked = [0] * self.Graph.getV()
        self.edgeTo = [0] * self.Graph.getV()
        self.marked[self.s] = True
        self.dfs(self.s)
        
    # Deep First Search recursive function
    def dfs(self,v): # Given a node
        self.marked[v] = True # It marks it as true (visited)
        # Then it visits if adjacent if they havent been visited yet
        for w in self.Graph.adj(v):
            if (self.marked[w] != True): 
                self.dfs(w)  # Visit unvisited node
                self.edgeTo[w] = v # Specify we get to node w from v
            
    def BreadthFirstSearch(self):
        # We explore the neightbours of the S and childs one by one
        queue = [self.s]
        self.marked = [0] * self.Graph.getV()
        self.edgeTo = [0] * self.Graph.getV()
        self.distTo = [0] * self.Graph.getV()
        self.marked[self.s] = True
        
        while (len(queue) !=  0): # While there are nodes in the queue
            v = queue.pop(0) # Node to explore
            for w in self.Graph.adj(v):
                if (self.marked[w] != True): 
                    queue.append(w)
                    self.marked[w] = True
                    self.edgeTo[w] = v
                    