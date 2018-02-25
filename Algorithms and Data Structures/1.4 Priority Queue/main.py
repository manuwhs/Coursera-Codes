# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
#import util as ul
import CMaxPQ as MPQ

########### MAIN  ######
keys = [9,12,32,4,5,3,25]

## Create heap with list

print "HeapSorting"
myMPQ = MPQ.CMaxPQ(keys,keys)
print myMPQ.keys

## Sorting in place 
#print "Sorting"
#myMPQ.sort()
#print myMPQ.keys


## Add the items to a already created heap
#print "Inserting"
#myMPQ = MPQ.CMaxPQ()
## Add all the keys with insert and they will get ordered.
#for k in keys:
#    myMPQ.insert(k,k)
#    
#print myMPQ.keys


#### Get all the keys in ordered manner deleting the highest element wach time
#print "Deleting Maximum"
#for k in keys:
#    print myMPQ.delMax()

