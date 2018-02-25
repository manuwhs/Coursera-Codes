# -*- coding: utf-8 -*-
"""
Created on Tue May  3 12:12:59 2016

@author: montoya
"""

import numpy as np
import UF as UF
import util as ul
########### MAIN  ######

N, data =  ul.load_connections("./UF_data.dat")

myUF = UF.CUF(N,mode = "QF")
myUF.set_initial_connections(data)
myUF.union(1,2)
myUF.union(6,2)
myUF.union(3,6)

print myUF.connected(2,4)

