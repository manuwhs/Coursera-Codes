# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
#import util as ul
import BST as BST

########### MAIN  ######
keys = [9,12,32,4,5,3,25,500,24]

## Create heap with list

print "Elementary Table Unordered"
myBST = BST.CBST()

for k in keys:
    myBST.put(k,k)
    
print myBST.getOrderedKeys()

print "min max"
print myBST.getMin()
print myBST.getMax()

print myBST.floor(28)
print myBST.ceil(21)

print myBST.getOrderedKeys()
print myBST.root.k
#keys = ['S', 'E','X','A','R','C','H','M']

#myBST = BST.CBST()
#
#for k in keys:
#    myBST.put(k,k)

#print myBST.sizeT()
print "Rank"
print myBST.rank(20)