# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import copy
from Node import CNode


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
    
    
class CBST():
    # Elemtary table of Key-value entries.
    # The list of keys is unordered

    @staticmethod  # Declare method as static
    def floor_node(n,k): # Finds the floor of a node 
        if (n == None):
            return None
        cmpare = compareTo(k, n.k)
        if (cmpare == 0):   # If it is equal
            return n
            
        elif(cmpare < 0):   # If it is lesser, it might be there
            return CBST.floor_node(n.nl,k)
            
        elif(cmpare > 0):
            t = CBST.floor_node(n.nr,k)
            if (t == None):
                return n
            else:
                return t
                
    @staticmethod  # Declare method as static
    def ceil_node(n,k): # Finds the floor of a node 
        if (n == None):
            return None
        cmpare = compareTo(k, n.k)
        if (cmpare == 0):
            return n
            
        elif(cmpare > 0):
            return CBST.ceil_node(n.nr,k)
            
        elif(cmpare < 0):
            t = CBST.ceil_node(n.nl,k)
            if (t == None):
                return n
            else:
                return t
                
    @staticmethod  # Declare method as static
    def size(n):    # Returns the size of the Node
        return n.c


    def __init__(self, root = None):  #create an empty priority queue
        if (root == None):
            self.root = CNode()
        else:
            self.root = root  # KEy of the node
        
        self.orderedKeys = []
     
        
    def get(self,k):  # If less go left, if more, go right
        # Number of compares is equal to 1 + depth of node.
        sn = self.root    # Search node initiallized at root
        while (sn != None): # While in the search we dont end the tree
            cmpare = compareTo(k, sn.k);
            
            if (cmpare == 0):
                return sn.v;
            elif(cmpare < 0):
                sn = sn.nl;
            elif (cmpare > 0):
                sn = sn.nr;
                
        return None
                
    def put(self,k,v):
        # Inserts a new node. It search for k, if it exists, it just replaces the value.
        # If it does not exist, it adds the new node where it should be:
        
        sn = self.root    # Search node initiallized at root
        lr_f = 0;  # Left, right flag to know at the end where we have to put the new node

        
        if(self.root.k == None): # If root empty
            self.root = CNode(k,v)
            
        while (1): # While in the search we dont end the tree
            cmpare = compareTo(k, sn.k);
            
            if (cmpare == 0):
                sn.v = v
                return sn.v;
                
            elif(cmpare < 0):
                if (sn.nl == None):
                    sn.c += 1
                    lr_f = 0
                    break;
                else:
                    sn.c += 1   # Add one count, we will be rooting it
                    sn = sn.nl;
                
            elif (cmpare > 0):  # 
                if (sn.nr == None):
                    sn.c += 1
                    lr_f = 1
                    break;
                else:
                    sn.c += 1
                    sn = sn.nr;
        # At the end of the while, if no match, sn is the node we append to its left or right the new key
        if (lr_f == 0):
            sn.nl = CNode(k,v)
        else:
            sn.nr = CNode(k,v)
            
        return sn.v
    
    
    def getNodesKeys(self,node):
        if(node.nl != None):
            self.getNodesKeys(node.nl)
        
        self.orderedKeys.append(node.v)
        if(node.nr != None):
            self.getNodesKeys(node.nr)
            
    def getMin(self):
        sn = self.root    # Search node initiallized at root
        while (1): # While in the search we dont end the tree
            if (sn.nl == None):
                return sn.k
            sn = sn.nl
    
    def getMinNode(self,s):
        # Gets the minimum node from a given node
        sn = s
        while (1): # While in the search we dont end the tree
            if (sn.nl == None):
                return sn
            sn = sn.nl
            
    def getMax(self):
        sn = self.root    # Search node initiallized at root
        while (1): # While in the search we dont end the tree
            if (sn.nr == None):
                return sn.k
            sn = sn.nr
            
    def getOrderedKeys(self):
        self.orderedKeys = []
        self.getNodesKeys(self.root)
        return copy.deepcopy(self.orderedKeys)
        
    def floor(self,k): # Returns the floor key to the query key k
        node = CBST.floor_node(self.root,k)
        return node.k
        
    def ceil(self,k): # Returns the floor key to the query key k
        node = CBST.ceil_node(self.root,k)
        return node.k

    def sizeT(self):
        return size(self.root)
    
    def rank(self,k):
        
        sn = self.root    # Search node initiallized at root
        rank_v = 0
        while (sn != None): # While in the search we dont end the tree
            cmpare = compareTo(k, sn.k);
            
            if (cmpare == 0):  # If found key, return the count of its left subtree
                if (sn.nl != None):  # We add its left children
                    rank_v += sn.nl.c ##size(sn.nl)
                    
                return rank_v
                
            elif(cmpare > 0):  # If it is inferior, we add its left part
                               # and check the right part
                rank_v += 1  # We add itself
                
                if (sn.nl != None):  # We add its left children
                    rank_v += sn.nl.c ##size(sn.nl)
                    
                sn = sn.nr;  # We go to its right place 
                
            elif (cmpare < 0): # If bigger we go to its left place
                sn = sn.nl
                
            
        return rank_v
    
    def delete(self,k):
        # First we find the key to delete, keepin track of its parent also
        sn = self.root
        sn_father = self.root    # Search node initiallized at root
        lr_f = -1;       # If it still -1l the node to delete is the root.
        
        
        # We find the father of the node to delete and weather is at its left or right.
        while (1): # While in the search we dont end the tree
            cmpare = compareTo(k, sn.k);

            if (cmpare == 0):  ## We delete it now !!
                break;
            
            elif(cmpare < 0):   # We have to go left
                if (sn.nl == None):
                    print "Key does not exist !! "
                    return -1
                else:
                    sn.c -= 1  # Lower count  
                    lr_f = 0   # The new key is ar left
                    sn_father = sn
                    sn = sn.nl
                    
            elif (cmpare > 0):  # 
                if (sn.nr == None):
                    print "Key does not exist !! "
                    return -1
                else:
                    sn.c -= 1  # Lower count  
                    lr_f = 1   # The new key is ar left
                    sn_father = sn
                    sn = sn.nr
                    
        # Now, sn_father has the parent of the node to delete and lr_f, the direction
        # CASES when 0 or 1 child

        if (sn.nl == None):    # Only right child or None
            print "STBWETRNBWR"
            print sn_father.k, lr_f, sn.k
            if(lr_f == 0):
                sn_father.nl = sn.nr
            elif(lr_f == 1):
                sn_father.nr = sn.nr
            elif(lr_f == -1):  # The node to delete 
                self.root = self.root.nr
            return 1
            
        if (sn.nr == None):    # Only left child or None
            if(lr_f == 0):
                sn_father.nl = sn.nl
            elif(lr_f == 1):
                sn_father.nr = sn.nl
            elif(lr_f == -1):  # The node to delete 
                self.root = self.root.nl
            return 1
        
        ## CASE Both Children
        # find smallest right child
        x = self.getMinNode(sn.nr)
        minR = copy.deepcopy(x)
        self.delete(x.k)
        
        minR.nl = sn.nl
        minR.nr = sn.nr
        # Remove it

        # Replace the removed
        if(lr_f == 0):
            sn_father.nl = minR
        elif(lr_f == 1):
            sn_father.nr = minR
        elif(lr_f == -1):  # The node to delete 
            self.root = minR
            
        sn.nl = minR.nr   
        
        return 1
    
