# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
#import util as ul
import ElemTable as ET
import ElemTableOrdered as ETO

########### MAIN  ######
keys = [9,12,32,4,5,3,25,500,24]

## Create heap with list

print "Elementary Table Unordered"
myET = ET.CElemTable(keys,keys)
print myET.keys

## Add the items to a already created heap
#print "Inserting"
# Add all the keys with insert and they will get ordered.

myET.insert(-12,56)
print myET.keys
print myET.values
myET.delete(32)
print myET.keys
print myET.values

print myET.min_k()

print "Elementary Table Ordered"
myETO = ETO.CElemTableOrdered()
for k in keys:
    myETO.insert(k,k)
print myETO.keys

