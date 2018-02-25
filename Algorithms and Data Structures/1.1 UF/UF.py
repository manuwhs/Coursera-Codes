# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np

class CUF():
    def __init__(self, N, mode = "QF"):
        self.N = N
        self.unions = []  # Empty unions structure
        self.QFid = range(N)
        self.QUid = range(N)
        self.mode = mode
        
    def set_initial_connections(self,nodes):
        # Nodes is a list of [p, q] values
        for pq in nodes:
            self.union(pq[0],pq[1])
    
    def root(self, i):  # Gets the root a node for the QU algo.
        while (self.QUid[i] != i):
            pass
        return i
        
    def union(self, p, q):    # Connects nodes p and q
        self.unions.append([p,q])
        
        if (self.mode == "QF"):
            changer = self.QFid[q]  # We change all the QFid[i] == QFid[p] by this one 
            toChange = self.QFid[p]
            for i in range(self.N):
                if (self.QFid[i] == toChange):
                    self.QFid[i] = changer
                    
        if (self.mode == "QU"):
            self.QUid[q] = self.QUid[self.root(p)]; # We make q a child of the root of p
            
            # We are creating clusters with the same id !!!!
            # All elements in a cluster are together.
      
    
    def connected(self,p,q): # Checks connection between p and q
        if (self.mode == "QF"):
            if (self.QFid[p] == self.QFid[q]):
                return 1 
            else:
                return 0
        if (self.mode == "QU"):
            if (self.QUid[self.root(p)] == self.QUid[self.root(q)]):
                return 1
            else:
                return 0



########### MAIN  ######

#N, data =  load_connections("./UF_data.dat")
#
#myUF = CUF(N)
##myUF.set_initial_connections(data)
#myUF.(1,2)
#myUF.union(6,2)
#myUF.union(3,6)
#
#print myUF.connected(2,4)

