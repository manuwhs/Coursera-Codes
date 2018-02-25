# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import copy

def compareTo(a,b):
    if(a > b):
        return 1;
    elif(a == b):
        return 0;
    elif(a < b):
        return -1
        
def less(a, b):    # Connects nodes p and q
    return compareTo(a,b) < 0
    
    
class CMergeSort():
        # Sortes vector v using the selection algorithm
    def __init__(self, v):
        self.v = v
        self.aux = copy.deepcopy(v)
        
        self.N = len(v)
        
    def sort(self, lo,hi):  # Sortd the self.v[lo:hi+1]
        # Sorts the part of the array
        # When reduced to 2 element sort, it also sorts using merge.
        if (hi <= lo):  # If we cannot split it anymore
            return;  
        # Divide and sort the splits
        mid = lo + (hi - lo)/2;
#        print lo,mid,hi
        self.sort(lo, mid);
        self.sort(mid+1, hi);
        
        # When the two halves are sorted we merge them
        self.merge(lo, mid, hi);
#        print self.v[lo:hi+1]
        
    def msort(self):
        self.sort(0,self.N-1)
        return self.v
        
    def merge2(v1,v2):
        # Merges the two sorted arrays into a merged one 
        L1 = len(v1)
        L2 = len(v2)
        
        merged =[]
        
        i = 0; j = 0
        for k in range (L1 + L2):
            if (v1[i] < v2[j]):
                merged.append(v1[i])
                i += 1
            else:
                merged.append(v2[j])
                j += 1
        
    def merge(self,lo,mid,hi):
        # Merges the two sorted array v[lo:mid] and v[mid:high] 
        # into the array aux[lo:high]
        
        # Indexes for both arrays 
        i = lo;  j = mid + 1;
        
#        print lo,mid,hi
#        print self.v[lo:hi]
#        print self.aux[lo:hi]
#
        self.aux = copy.deepcopy(self.v)
        
        for k in range(lo, hi +1): # For every position to order
        
        # Corner cases
            if (i > mid):
                self.v[k] = self.aux[j]
                j += 1
                
            elif (j > hi):
                self.v[k] = self.aux[i]
                i += 1
                
            elif (self.aux[i] < self.aux[j]):
                self.v[k] = self.aux[i]
                i += 1
            else:
                self.v[k] = self.v[j]
                j += 1

        
    def exch(self,i,j):  # Exchange positions i and j in the array
        aux = self.v[i]
        self.v[i] = self.v[j]
        self.v[j] = aux
        
