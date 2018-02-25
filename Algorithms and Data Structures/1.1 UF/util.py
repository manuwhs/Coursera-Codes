# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np

def load_connections(file_dir = "./data.txt"):
    fd = open(file_dir, mode = "r");
    data = fd.read()
    
    data = data.split("\n")  
    N = int(data[0])  # Get the number of nodes
    data = data[1:-1]   # Remove first element and last (because)
    
    unions = []
    for un in data:
        pq = un.split(" ")
#        print pq
        unions.append([int(pq[0]), int(pq[1])])
    
    return [N, unions]
