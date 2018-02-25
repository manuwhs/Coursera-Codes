# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import util as ul
import SelectionSort as SelS
import InsertionSort as InsS
import ShellSort as SheS
import KnuthShuffle as NnuSh
########### MAIN  ######

print "Selection Sort"
vec = [1, -2, 3, 4, -8, 9, 23, -1, 3, 4]
mySelS = SelS.CSelectionSort(vec)
print mySelS.sort()


print "Insertion Sort"
vec = [1, -2, 3, 4, -8, 9, 23, -1, 3, 4]
myInsS = InsS.CInsertionSort(vec)
print myInsS.sort()


print "Shell Sort"
vec = [1, -2, 3, 4, -8, 9, 23, -1, 3, 4]
mySheS = SheS.CShellSort(vec)
print mySheS.sort()

print "Knuth Shuffle"
vec = [1, -2, 3, 4, -8, 9, 23, -1, 3, 4]
myKnuSh = NnuSh.CKnuthShuffle(vec)
print myKnuSh.shuffle()

