# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import UF as UF

# Krustal Algo to compute the MST

class CKrustalMST(): # Computes MST
    def __init__(self, WGraph):
        self.Graph = WGraph
        self.MST = []; # List with the edges of the MST
        
    def compute(self): # is there a path from s to v?

        ## Order edges according to weight 
        
        ordered_edges = sorted(self.Graph.edges, key=lambda x: x[2]) ## Assume ordered 
#        print ordered_edges
        # Create the Union Find object used to check the connections
        myUF = UF.CUF(self.Graph.getV())
        
        i = 0;
        
        # While we havent process all ordered edges or
        # the number of edges in the MST is already V - 1
        while (i < len(ordered_edges)):
            e = ordered_edges[i]
            v1 = e[0]
            v2 = e[1]
            
            
            if (myUF.connected(v1, v2) == 0):  # If the nodes are not already connected
                myUF.union(v1, v2);
                self.MST.append(e);
#                print myUF.QFid
                # If we already found them all
                if (len(self.MST) == self.Graph.getV() - 1):
                    break;
            i+= 1;
            
        return self.MST