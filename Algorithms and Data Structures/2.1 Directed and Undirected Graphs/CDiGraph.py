# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np

class CGraph():
    def __init__(self, V, directed = False):  #create an empty graph with V vertices
        self.V = V  # Number of vertex 
        self.G = []   # G is a list of lists G[N][E]. It contains,for every Vertex, the nodes it is connected to.
        self.edges = []  # Just the list of all unique edges.
        self.D = directed # If the graph is directed or not 
        
        for i in range(self.V):
            self.G.append([])
    
    def getReverseGraph(self):
        RG = CGraph(self.V, self.D)
        RG.addReverseEdges(self.edges)
        return RG
        
    def addEdge(self,v1, v2):  # Adds an edge between edges v1 and v2
        self.G[v1].append(v2)   # Fill adj structure
        if (self.D == False):
            self.G[v2].append(v1)   # Only for Undirected Graphs
        
        self.edges.append([v1,v2])  # Fill edge structure
    
    def addReverseEdge(self,v1,v2):
        self.G[v2].append(v1)   # Fill adj structure
        
    def addReverseEdges(self,edges_list):
        for edge in edges_list:
            self.addReverseEdge(edge[1],edge[0])
        
    def removeEdge(self,v1,v2):
        self.G[v1].remove(v2)   # Fill adj structure
        if (self.D == False):   # If undirected
            self.G[v2].remove(v1)   # Only for Undirected Graphs
            
    def addEdges(self, edges_list): # Adds a list of edges 
     # Nodes is a list of [p, q] values
        for edge in edges_list:
            self.addEdge(edge[0],edge[1])
            
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
            print str(e[0]) +" - "+ str(e[1])
            





