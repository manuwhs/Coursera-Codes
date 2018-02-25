# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import copy

class CMinPQ():
    # Priority Queue using a Heap Ordered Binary Tree.
    # No need of graph representation.
    # Each node of the Binary tree is bigger than its descendants
    # We dont need tree representation.  Only array representation .
    # The childs of a node which is at position k are at positons 
    # 2*k + 1 and 2*k + 2 in the array of nodes.
    # a[k] > a[2*k + 1]  y a[k] > a[2*k + 2]. This is a necesary condition 
    # for the array to be ordered anyway.

    # For adding a new element, we put it in the last position and make it swim up
    # the place it belongs (like merge sort/ quick sort) ?

    # THE STRUCTURE ITSELF DOES NOT WARANTY THAT ALL THE KEYS ARE SORTED
    # TO obtain so, we delete the maximum
   

    def __init__(self, key_list = [], values_list = []):  #create an empty priority queue
        self.keys = copy.deepcopy(key_list)  # Array with the key values. (They get ordered)
        self.values = copy.deepcopy(values_list) # Array with the values associated to the keys
        self.N = len(key_list);     # Size of the queue
        
        if (self.N != 0):  # If the Binary Tree is initialized
            self.heapSort()  # Sorts the array in a heap way
    
    def less(self,i,j):
        ## CHANGED TO MAKE IT LESS
        # Returns true if the key of elemnt i  is lower than j
        return self.keys[i] > self.keys[j]
    
    def exch(self, i,j):
        # Exchange keys and values of postions i and j in the array
        key = self.keys[i]
        self.keys[i] = self.keys[j]
        self.keys[j] = key
        
        value = self.values[i]
        self.values[i] = self.values[j]
        self.values[j] = value
    
        
    def isEmpty(self):  # Returns True if empty
        return self.N == 0
        
    def heapSort(self):
        # Sorts the keys in the Heap way if they are not sorted.
        # For doing so, it just sinks the nodes bottom-up starting
        # by those nodes that have children
        
        print range(self.N/2,-1,-1)
        
        for k in range(self.N/2 +1,-1,-1):
            self.sink(k);       # Sink all the shallowest nodes
            
#    def sort(self):
#        # To return a sorted array we could keep removing the delMax() until
#        # the heap is empty or order it in place.
#    
#        for k in range(self.N - 1):
#            self.exch(0, k);
#            self.sink(0);
        
    def swim(self,k):
        # If a node is biger than its parent, we exchange it with it if we are
        # bigger than our node friend. We iterate until we cannot swim.
    
        k = int(k)
        # par_k = (k-1)/2  # Parent of the node
        # While we are not at the root and our parent is smaller than us
        while ((k > 0) and (self.less((k-1)/2,k))): #
            
            # Check if our friend is bigger. If so, break
            if (k%2 == 0):  # If it is odd. (it is the second node)
                if (self.less(k,k-1)): # If it is smaller than our friend
                    break;  # We dont promote it
            
            else:  # If it is odd and k+1 exists
                if (self.N > k+1):
                    if (self.less(k,k+1)): # If it is smaller than our friend
                        break;  # We dont promote it 
            self.exch(k, (k-1)/2);
            k = (k-1)/2
        

    def sink(self, k):
        # If a node is lower than its children, the node gets exchanged with
        # the highest of its descending  nodes.
    
        while (self.N > 2*k +1):  # While the sinked value has children
            # Child nodes are 2k+1 and 2k+2
            # Find the biggest child to exchange it with
            j = 2*k + 1;   # First child
            
            if (j+1 < self.N): # If the second child exists
                if (self.less(j,j+1)): # If the second child is bigger than the first
                    j += 1    # Select the second node
            
            # If the key was bigger than its descendants, do nothing
            if (self.less(j,k)):
                break;
#            print k,j
            self.exch(k, j);  # Exchange nodes k and j
            k = j   # Make k = j to iterate again and sink if necesary
    
    
    def insert(self,k,v = 0):  # Insert key and value
        # We insert it in the last position and make it swim up
        self.keys.append(k)
        self.values.append(v)
        
        self.N += 1
        self.swim(self.N - 1) # Make the last element swim
        
        
    def delMin(self):   # Return and remove the biggest item
        # To do so, we exchange its position in the pq with the smallest element,
        # and sink the smallest element to its new position.
        maxKey = self.keys[0]
        maxValue = self.values[0]
        
        self.exch(0, self.N -1)  # Exchange lowest and highest and sink highest
        
        self.keys.pop(self.N-1)  # Remove the key and its values from the list
        self.values.pop(self.N-1)
        self.N -= 1   # Decrease number of elements in the queue
        
        if (self.N > 0): # If not empty

            self.sink(0)  # Sink the values
        


        return [maxKey,maxValue]
    
    def sortBU(self):
        # If the keys are unsorted, this is an inplace sort that does it bottom up
        # making all the 
        print 3
    def size(self):    # Returns the size of the PQ
        return self.N
        
    def contains(self,v):
        # Checks if the Heap contains the value v
        for i in range(self.N):
            if (self.values[i] == v):
                return True
    
    def decreaseKey(self,v,k):  # Decrease the key value whose content is v
        for i in range(self.N):
            if (self.values[i] == v):
                self.keys[i] = k
                self.heapSort() # Fuck this shit and heapSort again