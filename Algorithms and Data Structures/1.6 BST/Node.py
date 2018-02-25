# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import copy

    
class CNode():
    # Elemtary table of Key-value entries.
    # The list of keys is unordered

    def __init__(self, k = None, v = None, nl = None, nr = None):  #create an empty priority queue
        self.k = k  # KEy of the node
        self.v = v   # Value fo the node
        self.nl = nl  # Left node
        self.nr = nr  # Right node
        self.c = 1    # Number of nodes rooted by this node
    
      