# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import copy
from CEdge import *

        
class CWGraph():
    def __init__(self, V, directed = False):  #create an empty graph with V vertices
        self.V = V  # Number of vertex 
        self.G = []   # G is a list of lists G[N]. It contains,for every Vertex, the edges objects it is connected to.
        self.edges = []  # Just the list of all unique edges. [v1,v2, weight]
        self.D = directed # If the graph is directed or not 
        
        for i in range(self.V):
            self.G.append([])
    
    def getReverseGraph(self):
        RG = CGraph(self.V, self.D)
        RG.addReverseEdges(self.edges)
        return RG
        
    def addEdge(self,v1,v2,w):  # Adds an edge between edges v1 and v2
        edge = CEdge(v1,v2,w)
        self.G[v1].append(copy.deepcopy(edge))   # Fill adj structure
        if (self.D == False):
            edge.reverse()
            self.G[v2].append(copy.deepcopy(edge))   # Only for Undirected Graphs
        
        self.edges.append([v1,v2,w])  # Fill edge structure
    
    def addReverseEdge(self,v1,v2,w):
        edge = CEdge(v2,v1,w)
        self.G[v2].append(copy.deepcopy(edge))
        
    def addReverseEdges(self,edges_list):
        for edge in edges_list:
            self.addReverseEdge(edge[1],edge[0], edge[2])
        
    def removeEdge(self,v1,v2): ## TODO
        self.G[v1].remove(v2)   # Find the edge whose vertex is v2
        if (self.D == False):   # If undirected
            self.G[v2].remove(v1)   # Only for Undirected Graphs
            
    def addEdges(self, edges_list): # Adds a list of edges 
     # Nodes is a list of [p, q] values
        for edge in edges_list:
            self.addEdge(edge[0],edge[1],edge[2])
            
    def adj(self, v):  # Gets list of vertices adjacent to v.
        return self.G[v]
        
    def getV(self):    # number of vertices
        return self.V
        
    def E(self):             # number of edges
        aux = 0
        for v in range(self.V):
            aux += len(self.adj[v])
        return aux/2
        
    def print_Edges(self):   # # Prints all possible unique edges
        for e in self.edges:
            print str(e[0]) +" - "+ str(e[1]) + ": w = " + str(e[2])
            





