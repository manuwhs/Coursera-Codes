# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np


def compareTo(a,b):
    if(a > b):
        return 1;
    elif(a == b):
        return 0;
    elif(a < b):
        return -1
        
def less(a, b):    # Connects nodes p and q
    return compareTo(a,b) < 0
    
    
class CSelectionSort():
        # Sortes vector v using the selection algorithm
    def __init__(self, v):
        self.v = v
    def sort(self):
        N = len(self.v)   # Length of the vector
        
        i = 0
        while(i < N -1):
            min_i = i
            
            j = i + 1
            while(j < N):
                if (less(self.v[j], self.v[min_i])):
                    min_i = j
                j+= 1;
            self.exch(i,min_i)
            i+= 1
            
        return self.v
        
    def exch(self,i,j):  # Exchange positions i and j in the array
        aux = self.v[i]
        self.v[i] = self.v[j]
        self.v[j] = aux
        


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

