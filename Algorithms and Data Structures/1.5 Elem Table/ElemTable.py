# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import copy

def compareTo(a,b):   # Compare to method
    if(a > b):
        return 1;
    elif(a == b):
        return 0;
    elif(a < b):
        return -1
        
def less(a, b):    # Connects nodes p and q
    return compareTo(a,b) < 0   
    
def equals(a,b):
    return compareTo(a,b) == 0
    
class CElemTable():
    # Elemtary table of Key-value entries.
    # The list of keys is unordered

    def __init__(self, key_list = [], values_list = []):  #create an empty priority queue
        self.keys = copy.deepcopy(key_list)  # Array with the key values. (They get ordered)
        self.values = copy.deepcopy(values_list) # Array with the values associated to the keys
        self.N = len(key_list);     # Size of the queue
        
    def exch(self, i,j):
        # Exchange keys and values of postions i and j in the array
        key = self.keys[i]
        self.keys[i] = self.keys[j]
        self.keys[j] = key
        
        value = self.values[i]
        self.values[i] = self.values[j]
        self.values[j] = value
    
    def contains(self,k):   #Returns -1 if no object and the indx if there is
        # Checks if the Heap contains the value v
        if (self.isEmpty()):# If empty do nothing
            return -1;
            
        for i in range(self.N):
            if (equals(self.keys[i], k)):
                return i
        return -1
        
    def get(self,k):
        if (self.isEmpty()):# If empty do nothing
            return [];
            
        for i in range(self.N):  # Search the key
            if (equals(self.keys[i],k)):
                return self.values[i]
        
        return []
        
    def isEmpty(self):  # Returns True if empty
        return self.N == 0
                
    def insert(self,k,v = 0):  # Insert key and value
        # We insert it in the last position and make it swim up
        
        # Check for duplicate keys !!!
        indx = self.contains(k)
        if (indx > -1):       # If duplicate key, we substitute
            self.values[indx] = v
        else:                  # Else, we add
            self.keys.append(k)
            self.values.append(v)
        
        self.N += 1
    
    def delete(self,k):   # Remove by key
        indx = self.contains(k)
        if (indx > -1):       # If key exists, we substitute
            self.values.pop(indx)
            self.keys.pop(indx)            
            self.N -= 1
            return 1
        else:                  # Else, we do nothing
            return -1
        
    def size(self):    # Returns the size of the PQ
        return self.N
    
    ##################################################################
    ############### Other methods that are costly if unordered ##########################3
    
    def min_k(self): #gets the 
        aux = self.keys[0]        
        for i in range(1,self.N):
            if (compareTo(aux,self.keys[i]) > 0):
                aux = self.keys[i]
        return aux
    
    def max_k(self): #gets the 
        aux = self.keys[0]        
        for i in range(1,self.N):
            if (compareTo(aux,self.keys[i]) < 0):
                aux = self.keys[i]
        return aux 
        
    def deleteMax(self): #gets the 
        maxk = self.max_k()       
        self.delete(maxk)
    
    def deleteMin(self): #gets the 
        mink = self.min_k()       
        self.delete(mink)
      