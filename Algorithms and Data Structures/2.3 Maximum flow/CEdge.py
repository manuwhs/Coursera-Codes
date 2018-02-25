# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import copy

class CEdge():
    def __init__(self, v1,v2,c):  #create an empty graph with V vertices
        self.v1 = v1
        self.v2 = v2
        self.c = c   # Capacity of the edge
        self.f = 0
        
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
            
    ###############################################################
            ########## FLOW SHIT
            
    def capacity(self):
        return self.c
        
    def flow(self):
        return self.f
    
    def residualCapacityTo(self,v):  # Returns the residual capacity in each direction
        if (v == self.v2):   # Forward capaciy v -> w
            return self.c - self.f
            
        elif(v == self.v1):  # Backward capaciy w -> v
            return self.f
    
    def addResidualFlowTo(self,v, delta):
        if (v == self.v2):   # Add Forward flow v -> w
            self.f += delta
            
        elif(v == self.v1):  # Add Backward flow w -> v
            self.f -= delta
            
    def compareTo(self, edge_q):  # Compare edges by weight
        if(self.weight < edge_q.weight):
            return -1;
        elif (self.weight > edge_q.weight):
            return +1;
        else:
            return 0;
    
    def toString(self): # string representation
        print str(self.v1) + " - " + str(self.v2) + ": w = " + str(self.w)