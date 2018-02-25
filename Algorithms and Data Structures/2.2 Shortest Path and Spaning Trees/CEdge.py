# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import copy

class CEdge():
    def __init__(self, v1,v2,w):  #create an empty graph with V vertices
        self.v1 = v1
        self.v2 = v2
        self.w = w
    
    def reverse(self):
        aux = self.v1
        self.v1 = self.v2
        self.v2 = aux
        
    def vfrom(self):   # Source vertex
        return self.v1
    def vto(self):
        return self.v2
        
    def either(self):   # Source vertex
        return self.v1
    
    def other(self,vx):  # Return the other vertex to the one asked
        if (self.v1 == vx):
            return self.v2;
        elif (self.v2 == vx):
            return self.v1
        else:
            print "GRGWERBHWRTBEWRT"
            return -1
    def weight(self):
        return self.w
        
    def compareTo(self, edge_q):  # Compare edges by weight
        if(self.weight < edge_q.weight):
            return -1;
        elif (self.weight > edge_q.weight):
            return +1;
        else:
            return 0;
    
    def toString(self): # string representation
        print str(self.v1) + " - " + str(self.v2) + ": w = " + str(self.w)